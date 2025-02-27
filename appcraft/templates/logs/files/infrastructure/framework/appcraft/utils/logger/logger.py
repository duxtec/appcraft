import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

import structlog
from infrastructure.framework.appcraft.utils.logger.base import LoggerBase


class Logger(LoggerBase):
    def __init__(
        self,
        name="appcraft",
        level: Optional[LoggerBase.Level] = None,
        filename="info",
    ):
        self.log_dir = os.path.join("logs")
        os.makedirs(self.log_dir, exist_ok=True)

        super().__init__(name="appcraft", level=level, filename="info")

        structlog.stdlib.recreate_defaults()
        structlog.configure(
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
        )
        structlog.configure(
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(self.level),
        )
        self.console_logger = structlog.get_logger(name)

    def _setup_handlers(self):
        if self.app_manager.debug_mode:

            class StructlogHandler(logging.Handler):
                def emit(handler_self, record):
                    level = record.levelname.lower()
                    level = "exception" if level == "error" else level
                    if hasattr(self.console_logger, level):
                        getattr(self.console_logger, level)(
                            (record.getMessage().strip())
                        )

            console_handler = StructlogHandler()
            self.addHandler(console_handler)

        self._setup_file_handler()

    def _setup_file_handler(self):
        log_rotation = self.app_manager.environ_or_config(
            "log_rotation", "monthly"
        )

        log_mapping = {
            "execution": self._setup_execution_rotating_file_handler,
            "daily": self._setup_daily_rotating_file_handler,
            "monthly": self._setup_monthly_rotating_file_handler,
            "annual": self._setup_annual_rotating_file_handler,
        }

        log_rotation_setup = log_mapping.get(
            log_rotation, self._setup_daily_rotating_file_handler
        )

        log_rotation_setup()

    def _setup_execution_rotating_file_handler(self):
        start_time = self.app_manager.start_time

        date, time = start_time.split(" ")

        log_date_dir = os.path.join(self.log_dir, date)
        os.makedirs(log_date_dir, exist_ok=True)

        file = os.path.join(log_date_dir, f"{time.replace(':', '')}.log")
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)

        current_file = os.path.join(self.log_dir, "current.log")
        file_handler_current = logging.FileHandler(current_file)
        file_handler_current.setFormatter(self.formatter)
        self.addHandler(file_handler_current)

    def _setup_daily_rotating_file_handler(self):
        log_filename = os.path.join(self.log_dir, "daily.log")
        handler = TimedRotatingFileHandler(
            log_filename,
            when="midnight",
            interval=1,
            backupCount=7,
        )

        handler.suffix = "%Y-%m-%d.log"

        def custom_file_path_handler(log_path):
            date = log_path.split(".")[-2]
            print(log_path)
            print(date)

            year, month, day = date.split("-")

            log_date_dir = os.path.join(self.log_dir, f"{year}_{month}")
            os.makedirs(log_date_dir, exist_ok=True)

            return os.path.join(log_date_dir, f"{day}.log")

        handler.namer = custom_file_path_handler

        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def _setup_monthly_rotating_file_handler(self):
        log_filename = os.path.join(self.log_dir, "monthly.log")
        handler = TimedRotatingFileHandler(
            log_filename,
            when="midnight",
            interval=1,
            backupCount=12,
        )

        handler.suffix = "%Y-%m.log"

        def custom_file_path_handler(log_path):
            date = log_path.split(".")[-2]
            print("Data")
            print(date)

            year, month = date.split("-")

            log_date_dir = os.path.join(self.log_dir, f"{year}")
            os.makedirs(log_date_dir, exist_ok=True)

            return os.path.join(log_date_dir, f"{month}.log")

        handler.namer = custom_file_path_handler

        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def _setup_annual_rotating_file_handler(self):
        log_filename = os.path.join(self.log_dir, "annual.log")
        handler = TimedRotatingFileHandler(
            log_filename,
            when="midnight",
            interval=1,
            backupCount=5,
        )

        handler.suffix = "%Y.log"

        def custom_file_path_handler(log_path):
            year = log_path.split(".")[-2]

            os.makedirs(self.log_dir, exist_ok=True)

            return os.path.join(self.log_dir, f"{year}.log")

        handler.namer = custom_file_path_handler

        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def reset_current_log(self):
        current_file = os.path.join("logs", "current.log")

        if os.path.exists(current_file):
            os.remove(current_file)
