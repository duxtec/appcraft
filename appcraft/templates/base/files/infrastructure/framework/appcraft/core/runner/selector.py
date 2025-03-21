import importlib
import importlib.util
import os
from types import ModuleType
from typing import Any, List, Sequence

from prompt_toolkit.shortcuts import radiolist_dialog

from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.framework.appcraft.core.runner.discovery import (
    RunnerDiscovery,
)
from infrastructure.framework.appcraft.core.runner.themes import RunnerThemes


class RunnerSelector:
    def __init__(self, args: List[str] = []):
        self.args = args
        self.themes = RunnerThemes()

    def select_module(self, folder: str) -> ModuleType | None:
        modules = RunnerDiscovery.get_modules(folder)
        if len(modules) < 1:
            raise Exception("No modules found.")
        elif len(self.args) and self.args[0] in modules:
            selected_module_name = self.args.pop(0)
        elif len(modules) == 1:
            selected_module_name = modules[0]
        else:
            choices = [(module, module) for module in modules]
            selected_text = "Choose a Module to Load:"
            selected_module_name = self.choice(
                text=selected_text, values=choices
            )

        if not selected_module_name:
            return None

        filepath = os.path.join(folder, str(selected_module_name) + ".py")

        if not os.path.isfile(filepath):
            print(f'The file "{selected_module_name}" was not found.')
            return None

        modulename = os.path.splitext(os.path.basename(filepath))[0]
        spec = importlib.util.spec_from_file_location(modulename, filepath)
        if spec is None:
            raise Exception(f"Cannot load module from {filepath}")
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise Exception(f"Cannot load module from {filepath}")
        spec.loader.exec_module(module)

        self.selected_module = module
        return self.selected_module

    def select_app(self, module: ModuleType):
        apps = RunnerDiscovery.get_apps(module)

        app_map = {app.__name__: app for app in apps}

        if len(apps) < 1:
            raise Exception("No apps found.")

        if len(self.args):
            app_name = self.args[0]
            if app_name in app_map:
                app_name = self.args.pop(0)
                self.selected_app = app_map[app_name]
                return self.selected_app

        if len(apps) == 1:
            self.selected_app = apps[0]
            return self.selected_app

        choices = [(cls, cls.__name__) for cls in apps]
        selected_text = "Choose a App to run:"
        selected = self.choice(text=selected_text, values=choices)

        self.selected_app = selected

        return self.selected_app

    def select_method(self, app: type[AppRunnerInterface]):
        app = self.selected_app
        runners = RunnerDiscovery.get_app_runners(app)

        if len(runners) < 1:
            raise Exception("No runners found.")

        if len(self.args) and self.args[0] in runners:
            self.selected_method = getattr(
                self.selected_app(), self.args.pop(0)
            )
            return self.selected_method

        if len(runners) == 1:
            self.selected_method = getattr(self.selected_app(), runners[0])
            return self.selected_method

        choices = [(runner, runner) for runner in runners]
        selected_text = "Choose an Action to perform:"
        selected = self.choice(text=selected_text, values=choices)

        if selected:
            self.selected_method = getattr(self.selected_app(), selected)
            return self.selected_method

    def choice(
        self,
        text: str,
        values: Sequence[tuple[Any, str]],
        title: str = "Appcraft",
    ):
        return radiolist_dialog(
            title=title,
            text=text,
            values=values,
            style=self.themes.style,
        ).run()
