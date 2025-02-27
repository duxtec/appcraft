import ast
import inspect
import os
from types import ModuleType
from typing import Dict, List, Type

from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)


class RunnerDiscovery:
    @staticmethod
    def get_modules(folder: str) -> List[str]:
        modules = []
        py_files = [
            file for file in os.listdir(folder) if file.endswith(".py")
        ]

        for file in py_files:
            filepath = os.path.join(folder, file)
            if os.path.isfile(filepath):
                if RunnerDiscovery.file_contains_app_class(filepath):
                    modules.append(os.path.splitext(file)[0])

        return modules

    @staticmethod
    def get_apps(module: ModuleType) -> List[Type[AppRunnerInterface]]:
        apps = []
        for name, obj in module.__dict__.items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, AppRunnerInterface)
                and obj is not AppRunnerInterface
            ):
                apps.append(obj)
        return apps

    @staticmethod
    def get_app_runners(app: Type[AppRunnerInterface]) -> List[str]:
        runners = []
        for name, method in app.__dict__.items():
            if callable(method) and hasattr(method, "is_app_runner"):
                runners.append(name)
        return runners

    @staticmethod
    def get_args_kwargs(args_input: List) -> tuple[List, Dict]:
        args = []
        kwargs = {}

        iterator = iter(args_input)

        for arg in iterator:
            if "=" in arg:
                key, value = arg.split("=", 1)
                kwargs[key] = value
            else:
                args.append(arg)

        return args, kwargs

    @staticmethod
    def file_contains_app_class(file_path: str) -> bool:
        with open(file_path, "r") as file:
            node = ast.parse(file.read(), filename=file_path)
            for class_node in ast.walk(node):
                if isinstance(class_node, ast.ClassDef):
                    for base in class_node.bases:
                        if (
                            isinstance(base, ast.Name)
                            and (base.id == "AppRunnerInterface")
                            or (
                                isinstance(base, ast.Attribute)
                                and base.attr == "AppRunnerInterface"
                            )
                        ):
                            return True
        return False
