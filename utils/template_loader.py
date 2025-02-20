import os
from os import listdir
from typing import Type

from appcraft.templates.base.files.infrastructure.\
    framework.appcraft.utils.import_manager import (
        ImportManager,
    )
from appcraft.templates.template_abc import TemplateABC


class TemplateLoader:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.templates: list[Type[TemplateABC]] = []
        self.template_names: list[str] = []
        self.default_templates: list[Type[TemplateABC]] = []
        self.default_template_names: list[str] = []

        self._load_templates()

    def _load_templates(self) -> None:
        for dir in listdir(self.template_dir):
            if not os.path.isdir(os.path.join(self.template_dir, dir)):
                continue

            im = ImportManager("appcraft.templates")
            try:
                attributes = im.get_module_attributes(dir)

                for name, attribute in attributes.items():
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, TemplateABC)
                        and attribute is not TemplateABC
                    ):
                        template = attribute
                        if template.active:
                            self.templates.append(template)
                            self.template_names.append(template.name)
                            if template.default:
                                self.default_templates.append(template)
                                self.default_template_names.append(template.name)
            except Exception:
                pass
