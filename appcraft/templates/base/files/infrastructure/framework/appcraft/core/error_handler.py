import os
import sys
from typing import Any, Callable

from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.core.core_printer import CorePrinter
from infrastructure.framework.appcraft.core.package_manager.interface import (
    PackageManagerInterface,
)
from infrastructure.framework.appcraft.utils.logger.base import LoggerBase


class ErrorHandler:
    def __init__(
        self, package_manager: PackageManagerInterface, logger: LoggerBase
    ):
        self.package_manager = package_manager
        self.logger: LoggerBase = logger
        self.debug = AppManager().debug_mode

    def handle_import_error(
        self, error: Exception, action: Callable[..., Any]
    ) -> bool:
        try:
            tb = error.__traceback__
            for _ in range(2):
                if tb is not None:
                    tb = tb.tb_next
            error.__traceback__ = tb

            error_str = str(error)

            if "'" in error_str:
                parts = error_str.split("'")
                missing_package = parts[1]
                if len(parts) > 3:
                    self.handle_other_errors(error)
                    missing_package = parts[3]
            else:
                return False

            root_dirs = [
                d
                for d in os.listdir(".")
                if os.path.isdir(os.path.join(".", d))
            ]
            if missing_package.startswith(".") or any(
                missing_package.startswith(dir) for dir in root_dirs
            ):
                return False
        except Exception:
            return False

        if missing_package not in self.package_manager.attempted_packages:
            CorePrinter.packages_not_found([missing_package], error=error)
            CorePrinter.trying_to_install_the_packages()
            if not self.package_manager.requirements_installed:
                self.package_manager.install_requirements()
            self.package_manager.install_package(missing_package)
            try:
                _, exc_value, _ = sys.exc_info()
                if exc_value:
                    del exc_value
                action()
                return True
            except Exception:
                return False
        else:
            return False

    def handle_other_errors(self, error: Exception):
        tb = error.__traceback__

        total_levels = 0
        tb_temp = tb

        while tb_temp is not None:
            total_levels += 1
            tb_temp = tb_temp.tb_next

        max_remove = min(3, total_levels - 1)

        for _ in range(max_remove):
            if tb is not None:
                tb = tb.tb_next

        error.__traceback__ = tb

        self.logger.exception(error)

        if self.debug:
            message = None
        else:
            message = None

        CorePrinter.execution_error(message)
