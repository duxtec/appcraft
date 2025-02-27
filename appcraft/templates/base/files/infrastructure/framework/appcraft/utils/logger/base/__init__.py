import logging
from abc import ABC
from enum import Enum

from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.utils.logger.interface import (
    LoggerInterface,
)
from infrastructure.framework.appcraft.utils.printer import Printer


class LoggerBase(LoggerInterface, logging.Logger, ABC):
    class Level(Enum):
        CRITICAL = logging.CRITICAL
        FATAL = logging.FATAL
        ERROR = logging.ERROR
        WARN = logging.WARNING
        WARNING = logging.WARNING
        INFO = logging.INFO
        DEBUG = logging.DEBUG
        NOTSET = logging.NOTSET

    def __init__(self, name="appcraft", level=None, filename="info"):
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
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.filename = filename

        self._setup_handlers()

    def _setup_handlers(self):
        logging.getLogger().handlers.clear()
        self.handlers.clear()

        if AppManager().debug_mode:

            class ConsoleHandler(logging.Handler):
                def emit(self, record):
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
        self.exception = lambda *args, **kargs: None
        self.critical = self.exception
        self.info = self.exception
        self.debug = self.exception
        self.error = self.exception
        self.log = self.exception
        self.warn = self.exception
        self.warning = self.exception

    def reset_current_log(self):
        pass
