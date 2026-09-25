# Database templates (`sqlalchemy`, `mongodb`)

The simplest instance of the [interchangeable-sibling-adapters pattern](architecture.md#the-interchangeable-sibling-adapters-via-is_installed-pattern): the `Port` and its default fallback adapter already live in `base`, so neither `sqlalchemy` nor `mongodb` needs a shared base template of its own (unlike `flask`/`flask_api`/`flask_ui` or `web_scraping`'s family).

## Contract (`base`)

- `application/ports/database.py` — `DatabaseReaderPort` (`get`), `DatabaseWriterPort` (`create`/`update`/`update_where`/`update_by_id`/`delete`/`delete_by_id`/`delete_where`), and `DatabasePort(DatabaseReaderPort, DatabaseWriterPort)` combining both. All abstract, all `application/`-layer.
- `infrastructure/memory/adapter.py` — `MemoryAdapter(DatabasePort)`, the zero-dependency default used when no database template is installed.
- `infrastructure/database/provider.py` — `get_default_database_adapter()`/`set_default_database_adapter()`. Lives in `infrastructure/`, not `application/`, since resolving/constructing a concrete `Adapter` is infrastructure-layer work (see the `Provider` naming convention in [architecture.md](architecture.md#naming-and-layering-conventions)). `_ADAPTER_BACKENDS` maps `"sqlalchemy"`/`"mongodb"` to `(template_module, template_class, adapter_module, adapter_getter_name)`; `_resolve_default_adapter()` reads `config/app.toml`'s `default_database_adapter` to pick which installed backend wins when both are installed (falling back to whichever is installed if the configured one isn't, and to `MemoryAdapter()` if neither is). A repository that wants a *specific* backend regardless of this config should inject that backend's concrete adapter class directly instead of calling `get_default_database_adapter()`.

## `sqlalchemy` (active)

- `infrastructure/database/sqlalchemy/adapter.py` — `SQLAlchemyAdapter(DatabasePort)`, `get_sqlalchemy_adapter()` shared-singleton getter (so the provider above and a repository injecting the adapter directly get the *same* instance).
- `infrastructure/database/sqlalchemy/filter.py`, `infrastructure/database/sqlalchemy/models/{base,user}.py` — SQLAlchemy-specific filter translation and ORM models. There is no `App` ORM model here — that was a stale leftover from before the provider-based default was introduced and has been removed; the adapter is model-agnostic and works against whatever `TModel` a repository passes in.
- `application/use_cases/database/list/{tables,columns}.py` — introspection use cases (`ListTablesUseCase`, `ListColumnsUseCase`) that import `SQLAlchemyAdapter` directly rather than going through `DatabasePort`, since the whole point is inspecting the concrete SQLAlchemy engine/metadata — the accepted `application/` → `infrastructure/` exception described in [architecture.md](architecture.md#naming-and-layering-conventions).
- `presentation/cli/database.py`, `runners/main/database.py` — a single flat file each (not a folder), since there's currently only one use-case group.
- `config/database.toml` — its own config file, separate from `config/app.toml`'s `default_database_adapter` key (connection string, pool settings, etc).

## `mongodb` (active)

- `infrastructure/database/mongodb/adapter.py` — `MongoDBAdapter(DatabasePort)` (via `pymongo`), `get_mongodb_adapter()` shared-singleton getter, same shape as sqlalchemy's.
- `infrastructure/database/mongodb/filter.py`, `infrastructure/database/mongodb/seeder.py`.
- `domain/models/programmer.py` — a demo domain model specific to this template's seeded example data (unlike `sqlalchemy`, which reuses `base`'s generic `User` model).
- `runners/tools/programmers.py` — a demo runner seeding/listing `Programmer` records.
- `config/mongodb.toml` — note this is named after the *engine*, not the *concept* (unlike `sqlalchemy`'s `config/database.toml`) — a pre-existing inconsistency, not a convention to follow for new templates.

Both can be installed together (`appcraft init sqlalchemy mongodb`) — each remains fully usable via its own `get_*_adapter()`/concrete class, only `get_default_database_adapter()`'s pick between them is affected by `config/app.toml`.
