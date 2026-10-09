import importlib

from infrastructure.utils.logger import Logger

# The 'logs' template ships its own, richer Logger (structlog, rotating
# file handlers) — detected here at runtime via is_installed(), instead
# of being baked in at generation time, so this keeps working even if
# the template is added later via `appcraft add_template`. Falls back
# to the zero-dependency Logger above when 'logs' isn't installed.
_default_logger: Logger | None = None


def _load_logs_backend() -> type[Logger] | None:
    template_module = importlib.import_module(
        "infrastructure.framework.appcraft.templates.logs"
    )
    if not template_module.LogsTemplate.is_installed():
        return None

    # Not wrapped in try/except: if 'logs' is installed but its own
    # dependencies (structlog, ...) aren't actually pip-installed yet,
    # this raises ImportError like any other missing import — left to
    # propagate so the caller's own auto-install-and-retry handling
    # (ErrorHandler.handle_import_error, in Initializer.main()) can fix
    # it and call this again.
    logger_module = importlib.import_module(
        "infrastructure.utils.logger.logger"
    )
    return logger_module.StructlogLogger


def get_default_logger(name: str = "appcraft") -> Logger:
    global _default_logger

    if _default_logger is None:
        backend = _load_logs_backend() or Logger
        _default_logger = backend(name=name)

    return _default_logger
