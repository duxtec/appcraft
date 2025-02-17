import traceback

from infrastructure.framework.appcraft.core.app_manager import AppManager

try:
    from infrastructure.framework.appcraft.utils.component_printer\
        import ComponentPrinter
except Exception:
    from infrastructure.framework.appcraft.utils.printer\
        import Printer as ComponentPrinter


class CorePrinter(ComponentPrinter):
    domain = "core"

    @classmethod
    def program_started(cls):
        cls.title("Program started!", end="\n\n")

    @classmethod
    def pipenv_not_found(cls):
        cls.warning("Pipenv not found. Installing ...")

    @classmethod
    def packages_not_found(cls, packages=None, error=None):
        if not error:
            cls.warning("Package not found")
        else:
            cls.warning("Package not found", end=" ")
            tb = traceback.extract_tb(error.__traceback__)[-1]
            last_file, last_line, func_name, text = tb
            cls.warning(f"in {last_file}, line {last_line}")
        if packages:
            cls.warning("Missing packages:")
            for package in packages:
                print(f" • {package}")

    @classmethod
    def trying_to_install_the_packages(cls):
        cls.info("Trying to install the packages...")

    @classmethod
    def installation_success(cls):
        cls.success("Packages installed successfully.")

    @classmethod
    def installation_error(cls, error_message=None):
        if error_message:
            cls.error(error_message, end="\n\n")

        cls.error("Error installing packages.")
        cls.error("Please contact the developer.")
        cls.execution_duration()

    @classmethod
    def execution_error(cls, error_message=None):
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
        if AppManager.debug_mode():
            cls.info("Execution duration", end=": ")
            cls.print(AppManager.get_uptime())
