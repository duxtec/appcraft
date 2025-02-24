import os
import sys

from infrastructure.framework.appcraft.core.runner.selector import (
    RunnerSelector,
)


class Runner:
    def __init__(
        self,
        theme=None,
        app_folder=os.path.join("runner", "main"),
        args=sys.argv.copy(),
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

        args, kwargs = self.discovery.get_args_kwargs(self.selector.args)
        self.selected_method(*args, **kwargs)
        return True
