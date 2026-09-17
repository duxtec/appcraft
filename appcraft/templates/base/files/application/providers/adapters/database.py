import importlib

from application.ports.database import DatabasePort
from infrastructure.framework.appcraft.core.config import Config
from infrastructure.memory.adapter import MemoryAdapter

_default_database_adapter: DatabasePort | None = None

# Other templates that ship their own DatabasePort adapter (e.g.
# sqlalchemy, mongodb) are detected here at runtime via is_installed(),
# instead of being baked in at generation time — so this keeps working
# even if the template is added later via `appcraft add_template`. Each
# entry names the template module (for is_installed()) and the adapter
# module's own shared-singleton getter (e.g. get_sqlalchemy_adapter()) —
# reusing that singleton instead of constructing a fresh adapter here
# keeps this the SAME instance a repository gets when it injects the
# concrete adapter class directly.
_ADAPTER_BACKENDS: dict[str, tuple[str, str, str, str]] = {
    "sqlalchemy": (
        "infrastructure.framework.appcraft.templates.sqlalchemy",
        "SQLAlchemyTemplate",
        "infrastructure.database.sqlalchemy.adapter",
        "get_sqlalchemy_adapter",
    ),
    "mongodb": (
        "infrastructure.framework.appcraft.templates.mongodb",
        "MongoDBTemplate",
        "infrastructure.database.mongodb.adapter",
        "get_mongodb_adapter",
    ),
}


def _load_backend_adapter(name: str) -> DatabasePort | None:
    backend = _ADAPTER_BACKENDS.get(name)
    if backend is None:
        return None

    (
        template_module_name,
        template_class_name,
        adapter_module_name,
        adapter_getter_name,
    ) = backend

    try:
        template_module = importlib.import_module(template_module_name)
        template_class = getattr(template_module, template_class_name)

        if not template_class.is_installed():
            return None

        adapter_module = importlib.import_module(adapter_module_name)
        adapter_getter = getattr(adapter_module, adapter_getter_name)
        return adapter_getter()
    except Exception:
        return None


def _resolve_default_adapter() -> DatabasePort:
    # config/app.toml's default_database_adapter picks which installed
    # backend backs get_default_database_adapter() when more than one is
    # installed (e.g. sqlalchemy and mongodb together) — the other stays
    # fully usable, just not as this generic default. A repository that
    # wants a specific backend regardless of this config should inject
    # that backend's concrete adapter class directly instead of this
    # function.
    configured = Config().get("app").get("default_database_adapter")
    if configured not in _ADAPTER_BACKENDS:
        configured = "sqlalchemy"

    fallback_order = [configured] + [
        name for name in _ADAPTER_BACKENDS if name != configured
    ]

    for name in fallback_order:
        adapter = _load_backend_adapter(name)
        if adapter is not None:
            return adapter

    return MemoryAdapter()


def get_default_database_adapter() -> DatabasePort:
    """Returns the default adapter, shared across entrypoints."""
    global _default_database_adapter
    if _default_database_adapter is None:
        _default_database_adapter = _resolve_default_adapter()
    return _default_database_adapter


def set_default_database_adapter(adapter: DatabasePort) -> None:
    """Overrides the default adapter (e.g. in tests, or a specific runner)."""
    global _default_database_adapter
    _default_database_adapter = adapter
