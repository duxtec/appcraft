import os
import sys

from infrastructure.framework.appcraft.core.runner.discovery import (
    RunnerDiscovery,
)
from infrastructure.framework.appcraft.core.runner.selector import (
    RunnerSelector,
)
from infrastructure.framework.appcraft.core.runner.themes import RunnerThemes


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
        self.selected_method(*args, **kwargs)
        return True
