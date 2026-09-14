import json
import os
from pathlib import Path
from typing import Any

from infrastructure.framework.appcraft.utils.printer import Printer


class TemplateManager:
    TEMPLATES_FILE = (
        Path("infrastructure")
        / "framework"
        / "appcraft"
        / "templates"
        / "templates.json"
    )

    def __init__(self, target_dir: Path | None = None):
        self.target_dir = target_dir or Path("")

    def load_templates(self) -> dict[str, dict[str, Any]]:
        template_file = self.target_dir / self.TEMPLATES_FILE
        if os.path.exists(template_file):
            with open(template_file, "r", encoding="utf-8") as file:
                return json.load(file).get("installed_templates", {})
        return {}

    def save_templates(self, templates: dict[str, dict[str, Any]]):
        template_file = self.target_dir / self.TEMPLATES_FILE
        with open(template_file, "w", encoding="utf-8") as file:
            json.dump(
                {"installed_templates": templates},
                file,
                indent=4,
                default=str,
            )

    def add_template(self, template_data: dict[str, Any]):
        templates = self.load_templates()
        template_name = next(iter(template_data.keys()))

        if template_name in templates:
            Printer.warning(
                f"Template '{template_name}' is already installed."
            )
            return

        templates.update(template_data)
        self.save_templates(templates)
