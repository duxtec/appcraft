import ast
import inspect
import os
from abc import ABC
from types import ModuleType
from typing import Dict, List, Type

from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)


class RunnerDiscovery:
    @staticmethod
    def get_modules(folder: str) -> List[str]:
        modules: list[str] = []
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
        apps: List[type[AppRunnerInterface]] = []
        for _, obj in module.__dict__.items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, AppRunnerInterface)
                and obj is not AppRunnerInterface
                and not isinstance(obj, ABC)
            ):
                apps.append(obj)

        return apps

    @classmethod
    def get_app_runners(cls, app: type[AppRunnerInterface]) -> List[str]:
        runners: List[str] = []

        for name in dir(app):
            method = getattr(app, name, None)
            if callable(method) and hasattr(method, "is_app_runner"):
                runners.append(name)

        return runners

    @staticmethod
    def get_args_kwargs(
        args_input: List[str],
    ) -> tuple[List[str], Dict[str, str]]:
        args: List[str] = []
        kwargs: Dict[str, str] = {}

        iterator = iter(args_input)

        for arg in iterator:
            if "=" in arg:
                key, value = arg.split("=", 1)
                kwargs[key] = value
            else:
                args.append(arg)

        return args, kwargs

    @classmethod
    def file_contains_app_class(cls, file_path: str) -> bool:
        try:
            with open(file_path, "r") as file:
                """
                tree = ast.parse(file.read(), filename=file_path)
                hierarchy = RunnerClassExtractor.get_class_hierarchy(tree)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Subscript):
                        bases = RunnerClassExtractor.extract_subscript_base(
                            node, hierarchy
                        )

                return
                """
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

        except Exception:
            pass

        return False
