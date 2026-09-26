Application Layer
===================

The **Application Layer** orchestrates business logic: it sits between **Presentation** and **Domain**, coordinating use cases, translating data at the boundary (via mappers and schemas), and depending on abstract contracts (**Ports**) instead of concrete infrastructure. It depends only on the **Domain Layer** — never on a specific framework, database driver, or delivery mechanism.

.. note::
    Older versions of this documentation (and two not-yet-migrated templates, ``git``/``github``) described this layer around an ``application/services/`` folder and an ``AdapterInterface`` suffix. That convention has been fully replaced by the one below — ``application/use_cases/`` + ``Port`` — across every active template except those two. Don't use ``application/services/`` as a reference for new code.

What belongs here
------------------

- **Use Cases** (``application/use_cases/<concept>/<name>.py``) — one class per operation, each with a single ``execute()`` method.
- **Ports** (``application/ports/<concept>.py``) — abstract contracts for something the application depends on but doesn't implement itself (a database, a browser engine, an external API).
- **Repositories** (``application/repositories/``) — orchestrate a ``Port`` for one specific domain model.
- **Mappers** (``application/mappers/``) — convert between domain models and schemas.
- **Schemas** (``application/schemas/input/``, ``application/schemas/output/``) — the data shapes exchanged with the **Presentation Layer**, kept separate from domain models so each can evolve independently.

What to avoid here
-------------------

- **Business rules that belong on the domain model.** The Application Layer orchestrates; it shouldn't decide what makes data valid — that's the **Domain Layer**'s job.
- **Direct interaction with the Presentation Layer.** A use case returns data; it never renders or formats it for a specific output.
- **Persistence logic.** A use case calls a ``Repository``, never a database driver directly — that's what the ``Port``/``Adapter`` split is for.
- **Depending on a concrete infrastructure class when a ``Port`` would do.** Two accepted exceptions: introspection-style use cases whose whole point is inspecting a specific implementation (e.g. listing a SQLAlchemy database's own tables) — see `Introspection use cases`_ — and use cases that just need "whichever implementation is currently installed," via a **Provider** — see `Providers <../infrastructure/index.html#providers>`_ on the Infrastructure Layer page.

Naming conventions
-------------------

- **``Port`` suffix** — an abstract contract, subclassing the shared ``Port`` ABC (``application/ports/__init__.py``), one file per concept at ``application/ports/<concept>.py``. This is the layer where interchangeable implementations plug in.
- **``Adapter`` suffix** *(Infrastructure Layer, covered on its own page)* — a concrete implementation of a ``Port``.
- **``Repository`` suffix** — orchestrates a ``Port`` for one domain model.
- **``UseCase`` suffix** — a single ``execute()`` method, one class per operation.
- **``Mapper`` suffix** — converts between a domain model and a schema.
- **``Schema`` suffix** — a Pydantic-backed data shape for the Presentation boundary.

Example: a Port
-----------------

``application/ports/database.py`` defines the contract every database engine (SQLAlchemy, MongoDB, or the in-memory default) implements:

.. code-block:: python

    from abc import ABC, abstractmethod
    from typing import Sequence, Type

    from application.ports import Port
    from domain.filters.interface import FilterInterface
    from domain.models import NewModel
    from domain.types.model import TModel


    class DatabaseReaderPort(Port, ABC):
        @abstractmethod
        def get(
            self,
            model: Type[TModel],
            filters: Sequence[FilterInterface] | None = None,
        ) -> list[TModel]:
            pass


    class DatabaseWriterPort(Port, ABC):
        @abstractmethod
        def create(self, model: type[TModel], entity: NewModel) -> TModel:
            pass

        # ... update, update_by_id, delete, delete_by_id, update_where, delete_where


    class DatabasePort(DatabaseReaderPort, DatabaseWriterPort, ABC):
        pass

A concrete engine implements this once (``infrastructure/database/sqlalchemy/adapter.py``'s ``SQLAlchemyAdapter(DatabasePort)``, or the zero-dependency ``infrastructure/memory/adapter.py``'s ``MemoryAdapter(DatabasePort)`` a fresh project starts with) — see the `Infrastructure Layer <../infrastructure/index.html>`_.

Example: a Repository
-----------------------

A ``Repository`` wraps a ``Port`` for one specific model, so use cases don't need to know which database engine is behind it. ``application/repositories/user.py``:

.. code-block:: python

    from application.ports.database import DatabasePort
    from application.repositories import RepositoryBase
    from domain.filters.interface import FilterInterface
    from domain.models.user import NewUser, User


    class UserRepository(RepositoryBase[User, NewUser]):
        def __init__(self, adapter: DatabasePort) -> None:
            self.adapter = adapter

        def get(self, filters: list[FilterInterface]):
            return self.adapter.get(self.model, filters)

        def create(self, entity: NewUser):
            return self.adapter.create(self.model, entity)

The base ``RepositoryBase``/``GenericRepository`` classes (``application/repositories/__init__.py``) already implement the mechanical parts (``update``, ``delete``, ``update_by_id``, ``delete_by_id``) in terms of the injected ``adapter`` — a concrete repository like ``UserRepository`` doesn't need to set ``model``/``new_model`` itself (``RepositoryBase[User, NewUser]``'s subscript already derives both automatically), and usually only overrides ``get``/``create`` if there's model-specific logic.

Example: a Mapper and Schema
------------------------------

``application/schemas/output/user.py`` defines the shape returned to the Presentation Layer:

.. code-block:: python

    from application.schemas import Schema


    class UserOutSchema(Schema):
        id: int
        username: str

``application/mappers/user.py`` converts a ``User`` domain model into it — the shared ``BaseMapper`` (``application/mappers/bases/__init__.py``) already implements ``to_schema``/``to_domain`` via Pydantic's own validation, so a concrete mapper is usually a one-liner:

.. code-block:: python

    from application.mappers.bases import BaseMapper
    from application.schemas.output.user import UserOutSchema
    from domain.models.user import User


    class UserMapper(BaseMapper[User, UserOutSchema]):
        pass

Example: a Use Case
----------------------

``application/use_cases/user/get.py`` — two use cases built on the framework's generic ``ReadUseCase``/``ReadOneUseCase`` (``application/use_cases/__init__.py``), each taking a ``UserRepository`` and returning ``UserOutSchema``:

.. code-block:: python

    from typing import Sequence

    from application.mappers.user import UserMapper
    from application.repositories.user import UserRepository
    from application.schemas.output.user import UserOutSchema
    from application.use_cases import ReadOneUseCase, ReadUseCase
    from domain.filters import EqualFilter
    from domain.filters.interface import FilterInterface
    from domain.models.user import User, UserId


    class ReadUserUseCase(ReadUseCase[UserOutSchema]):
        def __init__(self, repository: UserRepository):
            self.repository = repository

        def execute(
            self, input_data: Sequence[FilterInterface]
        ) -> list[UserOutSchema]:
            users = self.repository.get(filters=input_data)
            return [UserMapper.to_schema(user) for user in users]


    class ReadOneUserUseCase(ReadOneUseCase[UserId, UserOutSchema]):
        def __init__(self, repository: UserRepository):
            self.repository = repository

        def execute(self, input_data: UserId) -> UserOutSchema:
            users = self.repository.get(
                filters=[EqualFilter(User.id, input_data)]
            )
            return UserMapper.to_schema(users[0])

Notice the full chain: a ``UseCase`` calls a ``Repository``, which calls a ``Port`` (implemented by whichever ``Adapter`` is actually installed), and converts the result through a ``Mapper`` into a ``Schema`` before it ever reaches the **Presentation Layer**.

Introspection use cases
--------------------------

The one accepted exception to "depend on a ``Port``, not a concrete ``Adapter``": a use case whose entire purpose is inspecting a *specific* implementation — for example, listing the tables of whichever SQLAlchemy database is connected. That can't be expressed against the generic ``DatabasePort`` (a MongoDB backend has no "tables"), so it's allowed to import the concrete ``SQLAlchemyAdapter`` directly instead.
