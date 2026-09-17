from typing import Any, Sequence, Type, cast
from uuid import uuid4

from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports.database import DatabasePort
from domain.filters.interface import FilterInterface
from domain.models import Model, NewModel
from domain.models.exceptions import ModelNotFoundError
from domain.types.model import TModel
from domain.value_objects.base import IntValueObject, ValueObjectBase
from domain.value_objects.id import Id
from domain.value_objects.id.uuid import UuidId
from infrastructure.database.mongodb.filter import FilterMongoDB
from infrastructure.framework.appcraft.core.config import Config


class MongoDBAdapter(DatabasePort):
    def __init__(
        self,
        uri: str | None = None,
        database: str | None = None,
    ):
        self.config = Config().get("mongodb")
        self.uri = uri or self.config["MONGODB_URI"]
        self.database_name = database or self.config["MONGODB_DATABASE"]

        self.client: MongoClient[dict[str, Any]] = MongoClient(self.uri)
        self.db = self.client[self.database_name]
        self._filter = FilterMongoDB()

    # ---------------------------------------------------------------
    # DatabasePort
    # ---------------------------------------------------------------

    def get(
        self,
        model: Type[TModel],
        filters: Sequence[FilterInterface] | None = None,
    ) -> list[TModel]:
        collection = self._collection(model)
        query = self._filter.build_query(filters or [])

        return [
            self._to_domain(model, document)
            for document in collection.find(query)
        ]

    def create(self, model: Type[TModel], entity: NewModel) -> TModel:
        collection = self._collection(model)

        generated_id = self._generate_id(model)
        domain_entity = model(id=generated_id, **entity.model_dump())

        collection.insert_one(self._to_document(domain_entity))
        return domain_entity

    def update(self, model: Type[TModel], entity: TModel) -> TModel:
        collection = self._collection(model)
        document = self._to_document(entity)

        result = collection.replace_one(
            {"_id": document["_id"]}, document
        )

        if result.matched_count == 0:
            raise ModelNotFoundError(model)

        return entity

    def update_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
        changes: Changes,
    ) -> TModel:
        collection = self._collection(model)

        update = {
            field.name: self._unwrap_value(value)
            for field, value in changes.items()
        }

        document = collection.find_one_and_update(
            {"_id": self._id_to_mongo(id)},
            {"$set": update},
            return_document=ReturnDocument.AFTER,
        )

        if document is None:
            raise ModelNotFoundError(model)

        return self._to_domain(model, document)

    def update_where(
        self,
        model: type[TModel],
        filters: Sequence[FilterInterface],
        changes: Changes,
    ) -> int:
        collection = self._collection(model)
        query = self._filter.build_query(filters)

        update = {
            field.name: self._unwrap_value(value)
            for field, value in changes.items()
        }

        result = collection.update_many(query, {"$set": update})
        return result.modified_count

    def delete(self, model: type[TModel], entity: TModel) -> None:
        collection = self._collection(model)
        document = self._to_document(entity)

        result = collection.delete_one({"_id": document["_id"]})

        if result.deleted_count == 0:
            raise ModelNotFoundError(model)

    def delete_by_id(self, model: type[TModel], id: Id | Keys) -> None:
        collection = self._collection(model)

        result = collection.delete_one({"_id": self._id_to_mongo(id)})

        if result.deleted_count == 0:
            raise ModelNotFoundError(model)

    def delete_where(
        self,
        model: Type[TModel],
        filters: Sequence[FilterInterface] | None = None,
    ) -> int:
        collection = self._collection(model)
        query = self._filter.build_query(filters or [])

        result = collection.delete_many(query)
        return result.deleted_count

    # ---------------------------------------------------------------
    # Infra / helpers
    # ---------------------------------------------------------------

    def list_collections(self) -> list[str]:
        return self.db.list_collection_names()

    def _collection(
        self, model: Type[Model[Any]]
    ) -> Collection[dict[str, Any]]:
        return self.db[f"{model.__name__.lower()}s"]

    def _to_document(self, entity: Model[Any]) -> dict[str, Any]:
        data = {
            key: self._unwrap_value(value)
            for key, value in entity.model_dump().items()
        }
        data["_id"] = data.pop("id")
        return data

    def _to_domain(
        self, model: Type[TModel], document: dict[str, Any]
    ) -> TModel:
        data = dict(document)
        data["id"] = data.pop("_id")
        return model(**data)

    def _id_to_mongo(self, id: Id | Keys) -> Any:
        if isinstance(id, Id):
            return id.value

        values = tuple(value for _, value in id.items())
        return values if len(values) > 1 else values[0]  # type: ignore

    def _unwrap_value(self, value: Any) -> Any:
        """Domain value objects (e.g. Id subclasses) aren't BSON-native —
        unwrap to the primitive it holds.
        """
        if isinstance(value, ValueObjectBase):
            return cast(Any, value).value
        return value

    def _generate_id(self, model: Type[TModel]) -> Any:
        id_type = model.id.type

        if issubclass(id_type, UuidId):
            return id_type(uuid4())

        if issubclass(id_type, IntValueObject):
            counters = self.db["counters"]
            sequence_name = model.__name__.lower()

            counter = counters.find_one_and_update(
                {"_id": sequence_name},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
            if counter is None:
                # Unreachable in practice (upsert=True + AFTER always
                # returns the (created-or-updated) document) — narrows
                # the type for pyright, which can't see that guarantee.
                raise RuntimeError(
                    "Failed to generate an id: the counters collection "
                    "returned no document after an upsert."
                )
            return id_type(counter["seq"])

        raise TypeError(
            f"MongoDBAdapter does not know how to generate an id of type "
            f"'{id_type.__name__}' for model '{model.__name__}'. "
            f"Supported: int-based Id subclasses (auto-increment via a "
            f"counters collection) and UuidId (uuid4())."
        )


_default_mongodb_adapter: MongoDBAdapter | None = None


def get_mongodb_adapter() -> MongoDBAdapter:
    """Returns the shared MongoDBAdapter, reused across entrypoints —
    same role as get_default_database_adapter(), but always backed by
    MongoDB regardless of config/app.toml's default_database_adapter.
    Inject this (typed as MongoDBAdapter, not DatabasePort) in any
    repository that specifically wants document storage.
    """
    global _default_mongodb_adapter
    if _default_mongodb_adapter is None:
        _default_mongodb_adapter = MongoDBAdapter()
    return _default_mongodb_adapter
