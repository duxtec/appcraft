import os
import sys

from infrastructure.core.printer import CorePrinter
from infrastructure.core.runner.mode import (
    InvalidInputError,
    MissingInputError,
    set_interactive,
)

from infrastructure.core.runner.discovery import (
    RunnerDiscovery,
)
from infrastructure.core.runner.pause import wait_for_key
from infrastructure.core.runner.selector import (
    RunnerSelector,
)
from infrastructure.core.runner.themes import RunnerThemes


class RunnerExecutor:
    def __init__(
        self,
        theme: str = RunnerThemes.dark_style,
        app_folder: str = os.path.join("runner", "main"),
        args: list[str] | None = None,
    ):
        self.selector = RunnerSelector(
            args if args is not None else sys.argv[1:].copy(),
            theme=theme,
        )
        self.app_folder = app_folder
        self._configure_mode()
        self.selected_module = None
        self.selected_app = None
        self.selected_method = None
        self.selector.themes.apply_theme()

    def run(self) -> bool:
        self.selected_module = self.selector.select_module(self.app_folder)
        if not self.selected_module:
            return False

        self.selected_app = self.selector.select_app(self.selected_module)
        if not self.selected_app:
            return False

        self.selected_method = self.selector.select_method(self.selected_app)
        if not self.selected_method:
            return False

        args, kwargs = RunnerDiscovery.get_args_kwargs(self.selector.args)
        pause = self._should_pause(kwargs)
        try:
            self.selected_method(*args, **kwargs)
        except (MissingInputError, InvalidInputError) as error:
            CorePrinter.error(str(error))
            sys.exit(1)
        finally:
            if pause:
                wait_for_key()
        return True

    def _configure_mode(self) -> None:
        """Runs are interactive by default. `interactive=false` turns questions
        off: a missing or invalid argument is an error, and confirmations take
        their default. The flag is removed from the arguments the method gets."""
        overrides = [arg for arg in self.selector.args if arg.startswith("interactive=")]
        self.selector.args = [arg for arg in self.selector.args if not arg.startswith("interactive=")]

        interactive = True
        if overrides:
            interactive = overrides[-1].split("=", 1)[1].strip().lower() in ("true", "yes", "y", "1", "on")
        set_interactive(interactive)

    def _should_pause(self, kwargs: dict[str, str]) -> bool:
        override = kwargs.pop("pause", None)
        if override is not None:
            return override.strip().lower() in ("true", "yes", "y", "1", "on")
        return bool(getattr(self.selected_method, "pause_on_exit", False))
