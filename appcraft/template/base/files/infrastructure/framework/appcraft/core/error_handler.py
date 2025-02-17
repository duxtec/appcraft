import os
import sys

from infrastructure.framework.appcraft.core.app_manager import AppManager

from infrastructure.framework.appcraft.core.core_printer import CorePrinter


class ErrorHandler:
    def __init__(self, package_manager, logger):
        self.package_manager = package_manager
        self.logger = logger
        self.debug = AppManager.debug_mode()

    def handle_import_error(self, error, action):
        try:
            error_str = str(error)

            if "'" in error_str:
                parts = error_str.split("'")
                missing_package = parts[1]
                if len(parts) > 3:
                    missing_package = parts[3]
            else:
                self.handle_other_errors(error)

            root_dirs = [
                d for d in os.listdir(".")
                if os.path.isdir(os.path.join(".", d))
            ]
            if (
                missing_package.startswith(".")
                or any(missing_package.startswith(dir) for dir in root_dirs)
            ):
                self.handle_other_errors(error)
        except Exception:
            self.handle_other_errors(error)

        if missing_package not in self.package_manager.attempted_packages:
            CorePrinter.packages_not_found([missing_package], error=error)
            CorePrinter.trying_to_install_the_packages()
            if not self.package_manager.requirements_installed:
                self.package_manager.install_requirements()
            self.package_manager.install_package(missing_package)
            action()
            sys.exit()
        else:
            CorePrinter.packages_not_found([missing_package], error=error)
            CorePrinter.execution_error()
            sys.exit(1)

    def handle_other_errors(self, e):
        tb = e.__traceback__
        for _ in range(3):
            if tb is not None:
                tb = tb.tb_next
        e.__traceback__ = tb

        self.logger.exception(str(e))

        if self.debug:
            message = None
        else:
            message = None

        CorePrinter.execution_error(message)
        sys.exit(1)
