Infrastructure Layer
=====================

The **Infrastructure Layer** contains every concrete, external-facing implementation: database adapters, third-party API clients, file/browser automation, and the framework's own runtime utilities (``infrastructure/framework/appcraft/``, covered on the `Runner <../runner/index.html>`_ page). It's the only layer allowed to depend on external frameworks and libraries — that's the whole point of keeping it separate: swapping a database engine or an HTTP client means changing files here, not anywhere else.

What belongs here
------------------

- **Adapters** — concrete implementations of an **Application**-layer ``Port``.
- **Providers** — resolve which installed ``Adapter`` backs a ``Port`` by default at runtime (see `Providers`_ below).
- Framework-specific wiring (e.g. a web framework's app factory, if a template adds one).
- Anything that talks to the outside world: a database, a browser, a filesystem, a third-party API.

What to avoid here
-------------------

- **Business logic.** An adapter translates between a ``Port``'s contract and a specific backend's API — it doesn't decide business rules.
- **Being imported directly by the Domain Layer.** Domain code never imports from ``infrastructure/`` — dependencies point the other way.
- **Being imported directly by the Application Layer**, except through a ``Port`` — with two accepted exceptions: introspection-style use cases, and use cases that call a **Provider** to get "whichever implementation is currently installed" (see the `Application Layer <../application/index.html#what-to-avoid-here>`_ page).

Naming convention: ``Adapter``
--------------------------------

A concrete implementation of a ``Port`` uses the **``Adapter`` suffix**. It lives at ``infrastructure/<concept>/adapter.py`` when there's only one implementation, or ``infrastructure/<concept>/<engine>/adapter.py`` when several interchangeable engines exist for the same concept (e.g. ``infrastructure/database/sqlalchemy/adapter.py`` and a hypothetical ``infrastructure/database/mongodb/adapter.py`` side by side).

Example: the default database Adapter
----------------------------------------

Every fresh project starts with ``infrastructure/memory/adapter.py``'s ``MemoryAdapter`` — a zero-dependency, in-process implementation of ``DatabasePort`` (see the `Application Layer <../application/index.html>`_ page), used automatically until a real database template (``sqlalchemy``, ``mongodb``) is installed:

.. code-block:: python

    from typing import Sequence, Type

    from application.ports.database import DatabasePort
    from domain.filters.interface import FilterInterface
    from domain.models import NewModel
    from domain.types.model import TModel
    from infrastructure.memory.filter import FilterMemory
    from infrastructure.memory.storage import StorageMemory


    class MemoryAdapter(DatabasePort):
        def __init__(self):
            self._storage = StorageMemory()
            self._filter = FilterMemory()

        def get(
            self,
            model: Type[TModel],
            filters: Sequence[FilterInterface] | None = None,
        ) -> list[TModel]:
            model_storage = self._storage.get_model_storage(model)
            result = model_storage.data.copy()
            for filter in filters or []:
                result = self._filter.apply_filter(result, filter)
            return list(result.values())

        def create(self, model: Type[TModel], entity: NewModel) -> TModel:
            model_storage = self._storage.get_model_storage(model)
            # ... assigns an id, stores the entity, returns it
            ...

A real database engine implements the exact same ``DatabasePort`` contract against its own driver (SQLAlchemy's ``Session``, PyMongo's client, ...) — nothing above the ``Adapter`` (the ``Repository``, the ``UseCase``, the ``Presentation``) needs to know or care which one is actually running.

Providers
-----------

Some concepts (which database, which browser-automation engine) have more than one valid ``Adapter``, installable side by side. A **Provider** — a plain function, not a class, living at ``infrastructure/<concept>/provider.py`` (e.g. ``infrastructure/database/provider.py``, ``infrastructure/web_scraping/provider.py``) — resolves which one is actually active at runtime via each candidate template's own ``is_installed()``, re-checked on every call so it keeps working no matter when a sibling template was added or removed, unlike a one-shot decision made at generation time.

``infrastructure/database/provider.py``'s ``get_default_database_adapter()`` is the reference implementation: it picks between ``sqlalchemy``, ``mongodb``, and the in-memory default based on which are installed and a ``config/app.toml`` preference, falling back gracefully if a repository's chosen backend isn't available. A ``Repository`` or ``UseCase`` that specifically wants a particular engine, regardless of that default, can always inject the concrete ``Adapter`` class directly instead of going through a ``Provider``.
