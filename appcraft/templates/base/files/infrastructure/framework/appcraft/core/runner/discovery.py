import ast
import inspect
import os
from types import ModuleType
from typing import Type

from infrastructure.framework.appcraft.core.runner import Runner


class RunnerDiscovery:
    @staticmethod
    def get_modules(folder: str) -> list[str]:
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
    def get_apps(module: ModuleType) -> list[Type[Runner]]:
        apps: list[type[Runner]] = []
        for _, obj in module.__dict__.items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, Runner)
                and obj is not Runner
                and not inspect.isabstract(obj)
            ):
                apps.append(obj)

        return apps

    @classmethod
    def get_app_runners(cls, app: type[Runner]) -> list[str]:
        runners: list[str] = []

        for name in dir(app):
            method = getattr(app, name, None)
            if callable(method) and hasattr(method, "is_app_runner"):
                runners.append(name)

        return runners

    @staticmethod
    def get_args_kwargs(
        args_input: list[str],
    ) -> tuple[list[str], dict[str, str]]:
        args: list[str] = []
        kwargs: dict[str, str] = {}

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
                                and (base.id == "Runner")
                                or (
                                    isinstance(base, ast.Attribute)
                                    and base.attr == "Runner"
                                )
                            ):
                                return True

        except Exception:
            pass

        return False
