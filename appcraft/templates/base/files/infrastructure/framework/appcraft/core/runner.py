import ast
import importlib.util
import inspect
import os
import sys

from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style

from infrastructure.framework.appcraft.core.core_printer import CorePrinter
from infrastructure.framework.appcraft.core.app_runner import AppRunner
from infrastructure.framework.appcraft.utils.color import Color


class Runner:
    palette = Color.palette()
    darkcolor = palette["darkcolor"]
    lightcolor = palette["lightcolor"]
    brightcolor = palette["brightcolor"]
    dark_style = Style.from_dict(
        {
            # Background and text color for dialog
            "dialog": f"bg:{darkcolor[0][0]} {lightcolor[0][0]}",
            # Background and text color for the frame label
            "dialog frame.label": f"\
bg:{darkcolor[2][2]} {lightcolor[0][0]} bold",
            # Background and text color for the body
            "dialog.body": f"bg:{darkcolor[1][2]} {lightcolor[0][0]}",
            # Background color for the shadow
            "dialog shadow": f"{lightcolor[0][0]}",
            # Text color for selected radio item
            "radio-selected": f"fg:{darkcolor[2][2]} {darkcolor[2][2]}",
            # Text color for unselected radio item
            "radio": f"fg:{darkcolor[1][2]} {lightcolor[0][0]}",
        }
    )

    light_style = Style.from_dict(
        {
            # Background and text color for dialog
            "dialog": f"bg:{lightcolor[0][0]} {darkcolor[0][0]}",
            # Background and text color for the frame label
            "dialog frame.label": f"\
bg:{lightcolor[2][2]} {darkcolor[0][0]} bold",
            # Background and text color for the body
            "dialog.body": f"bg:{lightcolor[1][2]} {darkcolor[0][0]}",
            # Background color for the shadow
            "dialog shadow": f"{lightcolor[0][0]}",
            # Text color for selected radio item
            "radio-selected": f"fg:{lightcolor[2][2]} {darkcolor[2][2]}",
            # Text color for unselected radio item
            "radio": f"fg:{lightcolor[1][2]} {darkcolor[0][0]}",
        }
    )

    def __init__(self, theme=None, app_folder="runners/main", args=sys.argv):
        self.app_folder = app_folder
        self.selected_module = None
        self.selected_app = None
        self.selected_method = None
        self.apply_theme(theme)
        self.args = args

    def apply_theme(self, theme=None):
        self.custom_style = theme if theme is not None else self.dark_style
        if self.custom_style is self.dark_style:
            bgcolor = self.darkcolor[1][2].lstrip('#')
        else:
            bgcolor = self.lightcolor[1][2].lstrip('#')

        r = int(bgcolor[0:2], 16)
        g = int(bgcolor[2:4], 16)
        b = int(bgcolor[4:6], 16)

        hex_color = f"rgb:{r:02x}/{g:02x}/{b:02x}"
        try:
            print(f"\033]11;{hex_color}\007", end='')
        except Exception:
            pass

        print(f"\033]11;{hex_color}\007", end='')

    def remove_theme(self):
        try:
            print("\033]11;#000000\007", end='')
        except Exception:
            pass

    def file_contains_app_class(self, filepath):
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

    def get_modules(self):
        modules = []
        py_files = [
            file
            for file in os.listdir(self.app_folder)
            if file.endswith(".py")
        ]

        for file in py_files:
            filepath = os.path.join(self.app_folder, file)
            if os.path.isfile(filepath) and self.file_contains_app_class(
                filepath
            ):
                modules.append(os.path.splitext(file)[0])

        return modules

    def select_module(self):
        modules = self.get_modules()
        if len(modules) < 1:
            raise Exception("No modules found.")
        elif len(self.args) > 1 and self.args[1] in modules:
            selected_module_name = self.args.pop(1)
        elif len(modules) == 1:
            selected_module_name = modules[0]
        else:
            choices = [(module, module) for module in modules]
            selected_module_name = self.choice(
                text="Choose a Module to Load:",
                values=choices
            )

        if not selected_module_name:
            return None

        filepath = os.path.join(self.app_folder, selected_module_name + ".py")

        if not os.path.isfile(filepath):
            print(f'The file "{selected_module_name}" was not found.')
            return None

        modulename = os.path.splitext(os.path.basename(filepath))[0]
        spec = importlib.util.spec_from_file_location(modulename, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.selected_module = module
        return self.selected_module

    def get_apps(self):
        module = self.selected_module
        apps = []
        for name, obj in module.__dict__.items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, AppRunner)
                and obj is not AppRunner
            ):
                apps.append(obj)
        return apps

    def select_app(self):
        apps = self.get_apps()

        app_map = {app.__name__: app for app in apps}

        if len(apps) < 1:
            raise Exception("No apps found.")

        if len(self.args) > 1:
            app_name = self.args[1]
            if app_name in app_map:
                app_name = self.args.pop(1)
                self.selected_app = app_map[app_name]
                return self.selected_app

        if len(apps) == 1:
            self.selected_app = apps[0]
            return self.selected_app

        choices = [(cls.__name__, cls.__name__) for cls in apps]
        selected = self.choice(
            text="Choose a App to run:",
            values=choices
        )

        self.selected_app = selected

        return self.selected_app

    def get_app_runners(self):
        app = self.selected_app
        runners = []
        for name, method in app.__dict__.items():
            if callable(method) and hasattr(method, "is_app_runner"):
                runners.append(name)
        return runners

    def select_method(self):
        runners = self.get_app_runners()

        if len(runners) < 1:
            raise Exception("No runners found.")

        if len(self.args) > 1 and self.args[1] in runners:
            self.selected_method = getattr(self.selected_app(), self.args[1])
            return self.selected_method

        if len(runners) == 1:
            self.selected_method = getattr(self.selected_app(), runners[0])
            return self.selected_method

        choices = [(runner, runner) for runner in runners]
        selected = self.choice(
            text="Choose an Action to perform:",
            values=choices
        )

        if selected:
            self.selected_method = getattr(self.selected_app(), selected)
            return self.selected_method

    def choice(self, text, values, title="Appcraft"):
        return radiolist_dialog(
            title=title,
            text=text,
            values=values,
            style=self.custom_style,
        ).run()

    def run(self):
        self.selected_module = self.select_module()
        if self.selected_module:
            self.selected_app = self.select_app()
            if self.selected_app:
                self.selected_method = self.select_method()
                if self.selected_method:
                    self.selected_method()
                    return True

        CorePrinter.program_interrupted()
        sys.exit(0)
