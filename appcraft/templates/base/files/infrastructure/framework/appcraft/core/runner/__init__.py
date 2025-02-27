import os
import sys
from typing import List, Optional

from infrastructure.framework.appcraft.core.runner.discovery import (
    RunnerDiscovery,
)
from infrastructure.framework.appcraft.core.runner.selector import (
    RunnerSelector,
)
from prompt_toolkit.styles import Style


class Runner:
    def __init__(
        self,
        theme: Optional[Style] = None,
        app_folder: str = os.path.join("runner", "main"),
        args: List[str] = sys.argv[1:].copy(),
    ):
        self.selector = RunnerSelector(args)
        self.app_folder = app_folder
        self.selected_module = None
        self.selected_app = None
        self.selected_method = None
        self.selector.themes.apply_theme(theme)

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
