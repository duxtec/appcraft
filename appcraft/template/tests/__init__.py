import os
from appcraft.utils.template_abc import TemplateABC


class TestsTemplate(TemplateABC):
    @property
    def description(self):
        return """
Tests Template provides a testing framework for your application. \
It includes predefined test cases, mock data, and configurations for \
running unit and integration tests, ensuring that your application \
is thoroughly tested.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('tests/test_example.py')
        directory_exists = os.path.isdir('tests')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
