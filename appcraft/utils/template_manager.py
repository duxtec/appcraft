import os
import json


class TemplateManager:
    class Template:
        data_analysis = "data_analysis"
        database = "database"
        flask_ui = "flask_ui"
        locale = "locale"
        database = "database"

    TEMPLATE_DIR = "templates"
    PROJECT_DIR = "new_project"

    def __init__(self):
        self.dependencies = self.load_dependencies()

    def load_dependencies(self):
        dependencies_path = os.path.join(
            self.TEMPLATE_DIR, "dependencies.json"
        )
        if os.path.exists(dependencies_path):
            with open(dependencies_path) as f:
                return json.load(f)
        return {}

    def get_available_templates(self):
        return [
            name for name in os.listdir(self.TEMPLATE_DIR)
            if os.path.isdir(os.path.join(self.TEMPLATE_DIR, name))
        ]

    def get_installed_templates(self):
        installed_templates = [
            name for name in os.listdir(self.PROJECT_DIR)
            if os.path.isdir(os.path.join(self.PROJECT_DIR, name))
        ]
        return installed_templates

    def check_missing_dependencies(self):
        installed = set(self.get_installed_templates())
        missing_dependencies = {}

        for template in installed:
            required = self.dependencies.get(template, {}).get("requires", [])
            missing = [dep for dep in required if dep not in installed]
            if missing:
                missing_dependencies[template] = missing

        return missing_dependencies

    def check_extra_files(self):
        missing_files = []
        installed = set(self.get_installed_templates())

        for template in installed:
            extra_files = self.dependencies.get(template, {}).get("extra_files", [])
            for file in extra_files:
                file_path = os.path.join(self.PROJECT_DIR, file)
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

        return missing_files
