import os
from appcraft.utils.template_abc import TemplateABC


class SeleniumTemplate(TemplateABC):
    _status = TemplateABC.AvailableStatus.inactive

    @property
    def description(self):
        return """
Selenium Template provides a setup for automating web browser interactions. \
It includes pre-configured Selenium scripts and configurations, allowing you \
to easily automate tests or tasks in a web environment.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('selenium/driver.py')
        directory_exists = os.path.isdir('selenium')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
