import ast
import inspect
import os
from types import ModuleType
from typing import Dict, List, Type

from infrastructure.framework.appcraft.core.app_runner import AppRunner


class RunnerDiscovery:
    def get_modules(self, folder: str) -> List[ModuleType]:
        modules = []
        py_files = [
            file for file in os.listdir(folder) if file.endswith(".py")
        ]

        for file in py_files:
            filepath = os.path.join(folder, file)
            if os.path.isfile(filepath) and self.file_contains_app_class(
                filepath
            ):
                modules.append(os.path.splitext(file)[0])

        return modules

    def get_apps(self, module: ModuleType) -> List[Type[AppRunner]]:
        apps = []
        for name, obj in module.__dict__.items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, AppRunner)
                and obj is not AppRunner
            ):
                apps.append(obj)
        return apps

    def get_app_runners(self, app: Type[AppRunner]) -> List[str]:
        runners = []
        for name, method in app.__dict__.items():
            if callable(method) and hasattr(method, "is_app_runner"):
                runners.append(name)
        return runners

    def get_args_kwargs(self, args: List) -> tuple[List, Dict]:
        args = []
        kwargs = {}

        iterator = iter(args[1:])

        for arg in iterator:
            if "=" in arg:
                key, value = arg.split("=", 1)
                kwargs[key] = value
            else:
                args.append(arg)

        return args, kwargs

    def file_contains_app_class(self, filepath) -> bool:
        with open(filepath, "r") as file:
            node = ast.parse(file.read(), filename=filepath)
            for class_node in ast.walk(node):
                if isinstance(class_node, ast.ClassDef):
                    for base in class_node.bases:
                        if (
                            isinstance(base, ast.Name)
                            and (base.id == "AppRunner")
                            or (
                                isinstance(base, ast.Attribute)
                                and base.attr == "AppRunner"
                            )
                        ):
                            return True
        return False
