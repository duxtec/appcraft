import os
from appcraft.utils.template_abc import TemplateABC


class GitTemplate(TemplateABC):
    @property
    def description(self):
        return """
Git Template sets up a Git repository for version control. It includes \
pre-configured files like `.gitignore` and a default repository structure, \
ensuring that the project is ready to be tracked and managed with Git.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('.git/config')
        directory_exists = os.path.isdir('.git')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
