import json
import os
from typing import Optional


class TemplateManager:
    TEMPLATES_FILE: str = (
        "\
infrastructure/framework/appcraft/templates/templates.json"
    )

    def __init__(self, target_dir: Optional[str] = None):
        self.target_dir = target_dir or ""

    def load_templates(self):
        template_file = os.path.join(self.target_dir, self.TEMPLATES_FILE)
        if os.path.exists(template_file):
            with open(template_file, "r", encoding="utf-8") as file:
                return json.load(file).get("installed_templates", [])
        return []

    def save_templates(self, templates):
        template_file = os.path.join(self.target_dir, self.TEMPLATES_FILE)
        with open(template_file, "w", encoding="utf-8") as file:
            json.dump({"installed_templates": templates}, file, indent=4)

    def add_template(self, template_name):
        templates = self.load_templates()
        if template_name not in templates:
            templates.append(template_name)
            self.save_templates(templates)
        else:
            print(f"Template '{template_name}' is already installed.")
