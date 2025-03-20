import json
import os
from typing import Any, Dict, Optional


class TemplateManager:
    TEMPLATES_FILE: str = os.path.join(
        "infrastructure",
        "framework",
        "appcraft",
        "templates",
        "templates.json",
    )

    def __init__(self, target_dir: Optional[str] = None):
        self.target_dir = target_dir or ""

    def load_templates(self) -> Dict[str, Dict[str, Any]]:
        template_file = os.path.join(self.target_dir, self.TEMPLATES_FILE)
        if os.path.exists(template_file):
            with open(template_file, "r", encoding="utf-8") as file:
                return json.load(file).get("installed_templates", {})
        return {}

    def save_templates(self, templates: Dict[str, Dict[str, Any]]):
        template_file = os.path.join(self.target_dir, self.TEMPLATES_FILE)
        with open(template_file, "w", encoding="utf-8") as file:
            json.dump({"installed_templates": templates}, file, indent=4)

    def save_template(self, template_name: str, content: Dict[str, Any]):
        template_file = os.path.join(self.target_dir, self.TEMPLATES_FILE)
        file_content = self.load_templates()
        file_content[template_name] = content
        with open(template_file, "w", encoding="utf-8") as file:
            json.dump({"installed_templates": file_content}, file, indent=4)

    def add_template(self, template_data: Dict[str, Any]):
        templates = self.load_templates()
        template_name = next(iter(template_data.keys()))

        if template_name in templates:
            print(f"Template '{template_name}' is already installed.")
            return

        templates.update(template_data)
        self.save_templates(templates)
