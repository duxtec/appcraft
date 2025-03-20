import traceback
from typing import List, Optional

from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class CorePrinter(ComponentPrinter):
    DOMAIN = "core"

    @classmethod
    def program_started(cls):
        cls.title("Program started!", end="\n\n")

    @classmethod
    def package_manager_not_found(cls, package_manager: str) -> None:
        cls.warning(f"{package_manager} not found. Installing ...")

    @classmethod
    def packages_not_found(
        cls,
        packages: Optional[List[str]] = None,
        error: Optional[Exception] = None,
    ) -> None:
        if not error:
            cls.warning("Package not found")
        else:
            cls.warning("Package not found", end=" ")
            tb = traceback.extract_tb(error.__traceback__)
            if len(tb) > 0:
                last_file, last_line, _, _ = tb[-1]
                cls.warning(f"in {last_file}, line {last_line}", emoji=False)
        if packages:
            cls.warning("Missing packages:")
            for package in packages:
                print(f" • {package}")

    @classmethod
    def trying_to_install_the_packages(cls) -> None:
        cls.info("Trying to install the packages...")

    @classmethod
    def installation_success(cls) -> None:
        cls.success("Packages installed successfully.")

    @classmethod
    def installation_error(cls, error_message: Optional[str] = None) -> None:
        if error_message:
            cls.error(error_message, end="\n\n")

        cls.error("Error installing packages.")
        cls.error("Please contact the developer.")
        cls.execution_duration()

    @classmethod
    def execution_error(cls, error_message: Optional[str] = None):
        if error_message:
            cls.error(f"{error_message}", end="\n\n")

        cls.error("Error executing the program.")
        cls.error("Please contact the developer.")
        cls.execution_duration()

    @classmethod
    def program_interrupted(cls):
        print("")
        cls.info("Execution interrupted!", end="\n\n")
        cls.execution_duration()

    @classmethod
    def program_finished(cls):
        print("")
        cls.success("Execution finished!", end="\n\n")
        cls.execution_duration()

    @classmethod
    def execution_duration(cls):
        app_manager = AppManager()
        if app_manager.debug_mode:
            cls.info("Execution duration", end=": ")
            cls.print(app_manager.uptime)
