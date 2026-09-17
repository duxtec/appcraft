import os
from typing import Any, Sequence, Type, cast

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports.database import DatabasePort
from domain.filters.interface import FilterInterface
from domain.models import NewModel
from domain.models.core.field import Field
from domain.models.exceptions import ModelNotFoundError
from domain.types.model import TModel
from domain.value_objects.base import ValueObjectBase
from domain.value_objects.id import Id
from infrastructure.database.sqlalchemy.filter import FilterSQLAlchemy
from infrastructure.database.sqlalchemy.models.base import Base
from infrastructure.framework.appcraft.core.config import Config
from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)


class SQLAlchemyAdapter(DatabasePort):
    def __init__(
        self,
        db_uri: str | None = None,
        create_all: bool = True,
    ):
        self.config = Config().get("database")
        self.uri = db_uri or self.config["SQLALCHEMY_DATABASE_URI"]
        self.engine = create_engine(self.uri)
        self.inspector = inspect(self.engine)

        raw_modules = ImportManager(
            "infrastructure.database.sqlalchemy.models"
        ).get_module_attributes()

        self._orm_models = {
            attr_name: attr_value
            for module_attrs in raw_modules.values()
            for attr_name, attr_value in module_attrs.items()
            if attr_name != "Base"
        }

        if not self.inspector.get_table_names() and create_all:
            Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._external_session_factory: Any = None
        self._filter = FilterSQLAlchemy()

    # ---------------------------------------------------------------
    # DatabasePort
    # ---------------------------------------------------------------

    def get(
        self,
        model: Type[TModel],
        filters: Sequence[FilterInterface] | None = None,
    ) -> list[TModel]:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            query = session.query(orm_model)
            for filter in filters or []:
                query = self._filter.apply_filter(query, orm_model, filter)

            return [self._to_domain(model, row) for row in query.all()]

    def create(self, model: Type[TModel], entity: NewModel) -> TModel:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            row = orm_model(**entity.model_dump())
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_domain(model, row)

    def update(self, model: Type[TModel], entity: TModel) -> TModel:
        orm_model = self._get_orm_model(model)
        pks = model.primary_keys()

        with self.get_session() as session:
            row = session.get(orm_model, self._pk_values(entity, pks))

            if row is None:
                raise ModelNotFoundError(model)

            for field, value in entity.model_dump().items():
                setattr(row, field, self._unwrap_value(value))

            session.commit()
            session.refresh(row)
            return self._to_domain(model, row)

    def update_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
        changes: Changes,
    ) -> TModel:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            row = session.get(orm_model, self._id_to_pk(id))

            if row is None:
                raise ModelNotFoundError(model)

            for field, value in changes.items():
                setattr(row, field.name, value)

            session.commit()
            session.refresh(row)
            return self._to_domain(model, row)

    def update_where(
        self,
        model: type[TModel],
        filters: Sequence[FilterInterface],
        changes: Changes,
    ) -> int:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            query = session.query(orm_model)
            for filter in filters:
                query = self._filter.apply_filter(query, orm_model, filter)

            rows = query.all()
            for row in rows:
                for field, value in changes.items():
                    setattr(row, field.name, value)

            session.commit()
            return len(rows)

    def delete(
        self,
        model: Type[TModel],
        entity: TModel,
        keys: list[str] | None = None,
    ) -> None:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            filter_kwargs = {
                key: self._unwrap_value(getattr(entity, key))
                for key in keys or ["id"]
            }
            row = (
                session.query(orm_model)
                .filter_by(**filter_kwargs)
                .one_or_none()
            )

            if row is None:
                raise ModelNotFoundError(model)

            session.delete(row)
            session.commit()

    def delete_by_id(self, model: type[TModel], id: Id | Keys) -> None:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            row = session.get(orm_model, self._id_to_pk(id))

            if row is None:
                raise ModelNotFoundError(model)

            session.delete(row)
            session.commit()

    def delete_where(
        self,
        model: Type[TModel],
        filters: list[FilterInterface] | None = None,
    ) -> int:
        orm_model = self._get_orm_model(model)

        with self.get_session() as session:
            query = session.query(orm_model)
            for filter in filters or []:
                query = self._filter.apply_filter(query, orm_model, filter)

            rows = query.all()
            for row in rows:
                session.delete(row)

            session.commit()
            return len(rows)

    # ---------------------------------------------------------------
    # Infra / helpers
    # ---------------------------------------------------------------

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def use_external_session(self, session_factory: Any) -> None:
        """Delegates session creation to an externally managed factory
        (e.g. Flask-SQLAlchemy's scoped session), so the adapter reuses
        the framework's per-request session lifecycle instead of
        managing its own.
        """
        self._external_session_factory = session_factory

    def get_session(self) -> Session:
        if self._external_session_factory is not None:
            return self._external_session_factory()
        return self.Session()

    def get_tables(self):
        return self.inspector.get_table_names()

    def get_columns(self, table_name: str):
        return self.inspector.get_columns(table_name)

    def _get_orm_model(self, model: Type[TModel]):
        orm_model = self._orm_models.get(model.__name__)
        if orm_model is None:
            raise ValueError(
                f"No SQLAlchemy model registered for domain model "
                f"'{model.__name__}'."
            )
        return orm_model

    def _to_domain(self, model: Type[TModel], row: Any) -> TModel:
        columns = {c.name for c in row.__table__.columns}
        return model(**{col: getattr(row, col) for col in columns})

    def _id_to_pk(self, id: Id | Keys) -> Any:
        if isinstance(id, Id):
            return id.value

        values: tuple[Any, ...] = tuple(value for _, value in id.items())
        return values if len(values) > 1 else values[0]  # type: ignore

    def _pk_values(self, entity: Any, pks: Sequence[Field[Any]]) -> Any:
        values: tuple[Any, ...] = tuple(
            self._unwrap_value(getattr(entity, pk.name)) for pk in pks
        )
        return values if len(values) > 1 else values[0]  # type: ignore

    def _unwrap_value(self, value: Any) -> Any:
        """Domain value objects (e.g. Id subclasses) aren't a type the
        DBAPI driver knows how to bind — unwrap to the primitive it holds.
        """
        if isinstance(value, ValueObjectBase):
            return cast(Any, value).value
        return value

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, db_uri: str):
        if not db_uri:
            raise ValueError("Database URI cannot be empty.")

        if db_uri.startswith("sqlite:///"):
            db_file = db_uri.replace("sqlite:///", "")

            if not os.path.isabs(db_file):
                current_dir = os.getcwd()
                db_dir = os.path.join(
                    current_dir, "infrastructure", "database"
                )
                os.makedirs(db_dir, exist_ok=True)
                db_file = os.path.join(db_dir, db_file)

            self.__uri = f"sqlite:///{db_file}"
        else:
            self.__uri = db_uri


_default_sqlalchemy_adapter: SQLAlchemyAdapter | None = None


def get_sqlalchemy_adapter() -> SQLAlchemyAdapter:
    """Returns the shared SQLAlchemyAdapter, reused across entrypoints —
    same role as get_default_database_adapter(), but always backed by
    SQLAlchemy regardless of config/app.toml's default_database_adapter
    (e.g. when mongodb is also installed and configured as the default).
    Inject this (typed as SQLAlchemyAdapter, not DatabasePort) in any
    repository or integration that specifically needs the SQL adapter.
    """
    global _default_sqlalchemy_adapter
    if _default_sqlalchemy_adapter is None:
        _default_sqlalchemy_adapter = SQLAlchemyAdapter()
    return _default_sqlalchemy_adapter
