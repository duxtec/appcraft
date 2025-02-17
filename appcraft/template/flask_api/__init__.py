import os
from appcraft.utils.template_abc import TemplateABC


class FlaskAPITemplate(TemplateABC):
    @property
    def description(self):
        return """
Flask API Template is a pre-configured setup for building RESTful APIs using \
Flask. It includes routes, models, and basic configuration to get started \
with API development, simplifying the process of building backend services.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('flask_api/api.py')
        directory_exists = os.path.isdir('flask_api')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
