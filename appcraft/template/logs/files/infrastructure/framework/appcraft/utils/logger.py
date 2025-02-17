import logging
import os
from sys import exception
import structlog

from infrastructure.framework.appcraft.core.app_manager import AppManager


class Logger(logging.Logger):
    class Level:
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
        structlog.stdlib.recreate_defaults()
        structlog.configure(
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
        )
        self.console_logger = structlog.get_logger(name)

        if level:
            self.setLevel(level)
            structlog.configure(
                wrapper_class=structlog.make_filtering_bound_logger(level)
            )

        self.filename = filename

        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self._setup_handlers()

    def _setup_handlers(self):
        if AppManager.debug_mode():
            class StructlogHandler(logging.Handler):
                def emit(handler_self, record):
                    level = record.levelname.lower()
                    level = "exception" if level == "error" else level
                    if hasattr(self.console_logger, level):
                        getattr(
                            self.console_logger, level
                        )((record.getMessage().strip()))
            console_handler = StructlogHandler()
            self.addHandler(console_handler)

        self._setup_file_handler()

    def _setup_file_handler(self):
        start_time = AppManager.get_start_time()
        date, time = start_time.split(" ")

        log_dir = os.path.join("logs")
        os.makedirs(log_dir, exist_ok=True)

        log_date_dir = os.path.join(log_dir, date)
        os.makedirs(log_date_dir, exist_ok=True)

        file = os.path.join(log_date_dir, f"{time.replace(':', '')}.log")
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)

        current_file = os.path.join(log_dir, "current.log")
        file_handler_current = logging.FileHandler(current_file)
        file_handler_current.setFormatter(self.formatter)
        self.addHandler(file_handler_current)

    def reset_current_log(self):
        current_file = os.path.join("logs", "current.log")

        with open(current_file, "w"):
            pass
