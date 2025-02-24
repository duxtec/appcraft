import logging
import os
import sys

from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.core.core_printer import CorePrinter
from infrastructure.framework.appcraft.core.error_handler import ErrorHandler
from infrastructure.framework.appcraft.core.package_manager import (
    PackageManager,
)
from infrastructure.framework.appcraft.utils.printer import Printer


class Initializer:
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

            if level:
                self.setLevel(level)

            self.formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            self._setup_handlers()

        def _setup_handlers(self):
            logging.getLogger().handlers.clear()
            self.handlers.clear()

            if AppManager.debug_mode():

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
                                Printer.fatal(msg)

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

    def __init__(self, app_folder=os.path.join("runners", "main")):
        self.start_time = AppManager.get_start_time()

        self.package_manager = PackageManager()

        try:
            from infrastructure.framework.appcraft.utils.logger import Logger

            self.logger = Logger(name="appcraft", level=Logger.Level.ERROR)
        except Exception:
            self.logger = self.Logger(
                name="appcraft", level=self.Logger.Level.ERROR
            )

        self.logger.reset_current_log()

        self.error_handler = ErrorHandler(
            package_manager=self.package_manager, logger=self.logger
        )
        self.import_error = False

        self.app_folder = app_folder

    def await_for_key_to_finish(self):
        CorePrinter.print("")
        CorePrinter.warning("Press any key to exit...", end="\n\n")
        try:
            import msvcrt

            msvcrt.getch()
        except ImportError:
            import termios
            import tty

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def execute_runner(self):
        from infrastructure.framework.appcraft.core.runner import Runner

        runner = Runner(
            Runner.dark_style, app_folder=self.app_folder, args=sys.argv.copy()
        )

        try:
            module_path = os.path.join(
                "infrastructure",
                "framework",
                "appcraft",
                "utils",
                "message_manager.py",
            )
            if os.path.exists(module_path):
                from infrastructure.framework.appcraft.utils.message_manager import (
                    MessageManager,
                )

                MessageManager.build_locale_dir()

            CorePrinter.program_started()
            runner.run()
            CorePrinter.program_finished()
            self.await_for_key_to_finish()
        except ImportError as e:
            self.import_error = True
            self.error_handler.handle_import_error(e, self.main)
        except KeyboardInterrupt:
            CorePrinter.program_interrupted()
            self.await_for_key_to_finish()
        except Exception as e:
            self.error_handler.handle_other_errors(e)
            self.await_for_key_to_finish()
        finally:
            runner.remove_theme()

    def main(self):
        try:
            if self.package_manager.venv_is_active() and not self.import_error:
                self.execute_runner()
            else:
                self.package_manager.run_command(
                    f"python {' '.join(sys.argv)}"
                )
        except ImportError as e:
            self.import_error = True
            self.error_handler.handle_import_error(e, self.main)
        except KeyboardInterrupt:
            CorePrinter.program_interrupted()
            sys.exit(0)
        except Exception as e:
            self.error_handler.handle_other_errors(e)
