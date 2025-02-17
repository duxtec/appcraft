import os
from appcraft.utils.template_abc import TemplateABC


class FlaskUITemplate(TemplateABC):
    @property
    def description(self):
        return """
Flask UI Template is a pre-configured user interface framework for \
Flask applications. It provides a set of resources and templates for \
building dynamic web pages, making it easier to develop applications \
with a consistent and responsive design. The template includes elements \
such as routes for views, integration with static assets, and ready-to-use \
HTML files for customization, streamlining the process of creating user \
interfaces in Flask.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('infrastructure/framework/flask/app.py')
        directory_exists = os.path.isdir(
            'presentation/web/ui'
        )

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
