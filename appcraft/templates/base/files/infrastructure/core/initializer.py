import importlib
import os
import sys
from typing import LiteralString

from infrastructure.app.manager import AppManager
from infrastructure.core.error_handler import ErrorHandler
from infrastructure.core.package.manager import (
    PackageManagerBase,
)
from infrastructure.core.printer import CorePrinter
from infrastructure.utils.logger import Logger
from infrastructure.utils.logger.provider import (
    get_default_logger,
)


class Initializer:
    def __init__(
        self, app_folder: LiteralString = os.path.join("runners", "main")
    ):
        self.start_time = AppManager().start_time

        self.package_manager = PackageManagerBase()

        # The zero-dependency default, constructed directly rather than
        # through get_default_logger(): __init__ isn't wrapped in any
        # try/except (run/tools call `Initializer(...).main()` with
        # nothing catching a construction-time error), so it must not
        # risk the ImportError a missing 'logs' dependency could raise.
        # main() below is where that resolution — and its self-heal via
        # handler_import_error — actually happens.
        self.logger = Logger(name="appcraft")

        self.error_handler = ErrorHandler(
            package_manager=self.package_manager, logger=self.logger
        )
        self.import_error = False

        self.app_folder = app_folder

    def execute_runner(self):
        from infrastructure.core.runner.executor import (
            RunnerExecutor,
        )
        from infrastructure.core.runner.themes import (
            RunnerThemes,
        )

        from domain.app import Theme

        theme_style = (
            RunnerThemes.light_style
            if AppManager().theme is Theme.LIGHT
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
                    'infrastructure.utils.message_manager'
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
            runner.selector.themes.remove_theme()

    def main(self):
        try:
            # Re-resolves (cheaply, via the provider's own cache) on every
            # call, including the recursive one handler_import_error makes
            # after auto-installing a missing dependency — so a 'logs'
            # install whose own dependency wasn't pip-installed yet gets
            # picked up once that's fixed, instead of staying on the
            # zero-dependency default for the rest of the run.
            self.logger = get_default_logger(name="appcraft")

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
