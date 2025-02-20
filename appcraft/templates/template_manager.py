import json
import os


class TemplateManager:
    TEMPLATES_FILE = "\
infrastructure/framework/appcraft/templates/templates.json"

    @classmethod
    def load_templates(cls):
        if os.path.exists(cls.TEMPLATES_FILE):
            with open(cls.TEMPLATES_FILE, "r", encoding="utf-8") as file:
                return json.load(file).get("installed_templates", [])
        return []

    @classmethod
    def save_templates(cls, templates):
        with open(cls.TEMPLATES_FILE, "w", encoding="utf-8") as file:
            json.dump({"installed_templates": templates}, file, indent=4)

    @classmethod
    def add_template(cls, template_name):
        templates = cls.load_templates()
        if template_name not in templates:
            templates.append(template_name)
            cls.save_templates(templates)
        else:
            print(
                f"Template '{template_name}' is already installed."
            )
