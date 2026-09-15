import importlib

from application.ports.database import DatabasePort
from infrastructure.memory.adapter import MemoryAdapter

_default_database_adapter: DatabasePort | None = None


def _resolve_default_adapter() -> DatabasePort:
    # Other templates that ship their own DatabasePort adapter (e.g.
    # sqlalchemy) are detected here at runtime via is_installed(), instead
    # of being baked in at generation time — so this keeps working even if
    # the template is added later via `appcraft add_template`.
    try:
        sqlalchemy_template_module = importlib.import_module(
            "infrastructure.framework.appcraft.templates.sqlalchemy"
        )
        SQLAlchemyTemplate = sqlalchemy_template_module.SQLAlchemyTemplate

        if SQLAlchemyTemplate.is_installed():
            sqlalchemy_adapter_module = importlib.import_module(
                "infrastructure.database.sqlalchemy.adapter"
            )
            return sqlalchemy_adapter_module.SQLAlchemyAdapter()
    except Exception:
        pass

    return MemoryAdapter()


def get_default_database_adapter() -> DatabasePort:
    """Returns the default adapter, shared across entrypoints."""
    global _default_database_adapter
    if _default_database_adapter is None:
        _default_database_adapter = _resolve_default_adapter()
    return _default_database_adapter


def set_default__database_adapter(adapter: DatabasePort) -> None:
    """Overrides the default adapter (e.g. in tests, or a specific runner)."""
    global _default_database_adapter
    _default_database_adapter = adapter
