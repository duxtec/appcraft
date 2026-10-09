import logging
from abc import ABC
from enum import IntEnum
from typing import Any, Callable

from infrastructure.app.manager import AppManager
from infrastructure.utils.printer import Printer


class _SourceFilter(logging.Filter):
    """Fills in `record.source` when nothing set one already, so the
    formatter can always reference `%(source)s` — on a plain call it
    falls back to the logger's own name (e.g. "appcraft"); `Logger.named()`
    overrides it per call instead."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "source"):
            record.source = record.name
        return True


class Logger(logging.Logger, ABC):
    class Level(IntEnum):
        CRITICAL = logging.CRITICAL
        FATAL = logging.FATAL
        ERROR = logging.ERROR
        WARN = logging.WARNING
        WARNING = logging.WARNING
        INFO = logging.INFO
        DEBUG = logging.DEBUG
        NOTSET = logging.NOTSET

    def __init__(
        self,
        name: str = "appcraft",
        level: Level | None = None,
        filename: str = "info",
    ):
        super().__init__(name)

        if level:
            self.setLevel(level)
            logging.basicConfig(level=level)

        self.app_manager: AppManager = AppManager()

        if not level:
            try:
                level = self.Level[self.app_manager.log_level.upper()]
            except Exception:
                level = self.Level.WARNING

        self.setLevel(level.value)
        logging.basicConfig(level=level.value)
        logging.getLogger("asyncio").setLevel(level.value)

        self.formatter = logging.Formatter(
            "%(asctime)s - %(source)s - %(levelname)s - %(message)s"
        )

        self.filename = filename

        self.addFilter(_SourceFilter())

        self._setup_handlers()

    def named(self, name: str) -> "logging.LoggerAdapter[Logger]":
        """A view of this same logger — same handlers, same singleton
        — that shows `name` in place of the logger's own name on every
        line, e.g. `logger.named("user").info(...)` prints "user"
        instead of "appcraft". Any string works: a layer, a domain
        concept, whatever identifies the caller — nothing new is
        created or registered, just a disposable wrapper around `self`.
        """
        return logging.LoggerAdapter(self, {"source": name})

    def _setup_handlers(self):
        logging.getLogger().handlers.clear()
        self.handlers.clear()

        if AppManager().debug_mode:

            class ConsoleHandler(logging.Handler):
                def emit(self, record: Any):
                    try:
                        msg = self.format(record)

                        if record.levelno == logging.INFO:
                            Printer.info(msg)
                        elif record.levelno == logging.ERROR:
                            Printer.error(msg)
                        elif record.levelno == logging.DEBUG:
                            Printer.debug(msg)
                        elif record.levelno == logging.WARNING:
                            Printer.warning(msg)
                        elif record.levelno == logging.CRITICAL:
                            Printer.critical(msg)
                        elif record.levelno == logging.FATAL:
                            Printer.critical(msg)

                        print("")

                    except Exception:
                        self.handleError(record)

            console_handler = ConsoleHandler()
            console_handler.setFormatter(self.formatter)
            self.addHandler(console_handler)
        else:
            self._disable_logging_methods()

    def _disable_logging_methods(self):
        self.exception: Callable[..., None] = lambda *args, **kwargs: None
        self.critical = self.exception
        self.info = self.exception
        self.debug = self.exception
        self.error = self.exception
        self.log = self.exception
        self.warning = self.exception

    def reset_current_log(self):
        pass
