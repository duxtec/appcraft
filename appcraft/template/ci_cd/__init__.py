import os
from appcraft.utils.template_abc import TemplateABC


class CICDTemplate(TemplateABC):
    @property
    def description(self):
        return """
CI/CD Template is designed to automate the process of building, testing, \
and deploying applications. It sets up continuous integration and continuous \
deployment pipelines, ensuring that the application is always in a deployable \
state. This template integrates with various CI/CD tools.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('ci_cd/.gitlab-ci.yml')
        directory_exists = os.path.isdir('ci_cd')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
