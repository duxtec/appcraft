import importlib
import os
import sys
from typing import LiteralString

from infrastructure.framework.appcraft.app.manager import AppManager
from infrastructure.framework.appcraft.core.error_handler import ErrorHandler
from infrastructure.framework.appcraft.core.package.manager.base import (
    PackageManagerBase,
)
from infrastructure.framework.appcraft.core.printer import CorePrinter
from infrastructure.framework.appcraft.utils.logger.base import LoggerBase
from infrastructure.framework.appcraft.utils.logger.interface import (
    LoggerInterface,
)


class Initializer:
    class Logger(LoggerBase):
        pass

    def __init__(
        self, app_folder: LiteralString = os.path.join("runners", "main")
    ):
        self.start_time = AppManager().start_time

        self.package_manager = PackageManagerBase()

        self.logger: LoggerInterface = self.Logger(name="appcraft")

        self.error_handler = ErrorHandler(
            package_manager=self.package_manager, logger=self.logger
        )
        self.import_error = False

        self.app_folder = app_folder

    def await_for_key_to_finish(self):
        CorePrinter.print("")
        CorePrinter.warning("Press any key to exit...", end="\n\n")

        if sys.platform == "win32":
            try:
                import msvcrt

                msvcrt.getch()
            except Exception:
                pass
        else:
            import termios
            import tty

            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)

                try:
                    tty.setcbreak(fd)
                    sys.stdin.read(1)
                finally:
                    termios.tcsetattr(
                        fd,
                        termios.TCSANOW,
                        old_settings,
                    )

            except (termios.error, OSError, ValueError):
                pass

    def execute_runner(self):
        from infrastructure.framework.appcraft.core.runner.executor import (
            RunnerExecutor,
        )
        from infrastructure.framework.appcraft.core.runner.themes import (
            RunnerThemes,
        )

        theme_style = (
            RunnerThemes.light_style
            if AppManager().theme == "light"
            else RunnerThemes.dark_style
        )

        runner = RunnerExecutor(
            theme_style,
            app_folder=self.app_folder,
            args=sys.argv[1:].copy(),
        )

        try:
            locales_template_module = importlib.import_module(
                "infrastructure.framework.appcraft.templates.locales"
            )
            LocalesTemplate = locales_template_module.LocalesTemplate
            if LocalesTemplate.is_installed():
                message_manager_module = importlib.import_module(
                    'infrastructure.framework.appcraft.utils.message_manager'
                )

                MessageManager = getattr(
                    message_manager_module, 'MessageManager'
                )

                MessageManager.build_locale_dir()

            CorePrinter.program_started()
            if runner.run():
                CorePrinter.program_finished()
            else:
                CorePrinter.program_interrupted()

        except KeyboardInterrupt:
            CorePrinter.program_interrupted()
        except ImportError as error:
            self.handler_import_error(error)
        except Exception as error:
            self.handler_other_errors(error)
        finally:
            self.await_for_key_to_finish()
            runner.selector.themes.remove_theme()

    def main(self):
        try:
            logs_template_module = importlib.import_module(
                "infrastructure.framework.appcraft.templates.logs"
            )
            LogsTemplate = logs_template_module.LogsTemplate
            if LogsTemplate.is_installed():
                logger_module = importlib.import_module(
                    'infrastructure.framework.appcraft.utils.logger.logger'
                )

                Logger = getattr(logger_module, 'Logger')

                self.logger: LoggerInterface = Logger(name="appcraft")

            self.logger.reset_current_log()
            if (
                self.package_manager.venv_is_active()
                and not self.import_error
            ):
                self.execute_runner()
            else:
                command = ["python"]
                command.extend(sys.argv)
                self.package_manager.run_command(command)

        except KeyboardInterrupt:
            CorePrinter.program_interrupted()

        except ImportError as error:
            self.handler_import_error(error)

        except Exception as error:
            self.handler_other_errors(error)

    def handler_import_error(self, error: Exception):
        self.import_error = True
        if not self.error_handler.handle_import_error(error, self.main):
            self.handler_other_errors(error)

    def handler_other_errors(self, error: Exception):
        self.error_handler.handle_other_errors(error)
        sys.exit(1)
