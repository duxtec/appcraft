import os
from appcraft.utils.template_abc import TemplateABC


class BaseTemplate(TemplateABC):
    _default = True

    @property
    def description(self):
        return """
Base template providing essential files and configurations for a structured, \
scalable, and customizable project setup.
"""

    @classmethod
    def is_installed(cls):
        directory_exists = os.path.isdir('infrastructure/framework/appcraft')

        return directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
