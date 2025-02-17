import os
from appcraft.utils.template_abc import TemplateABC


class WebScrappingTemplate(TemplateABC):
    _status = TemplateABC.AvailableStatus.inactive

    @property
    def description(self):
        return """
Web Scrapping Template provides a setup for extracting data from websites. \
It includes pre-configured scripts for web scraping, as well as libraries for \
parsing HTML and handling web requests.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('web_scrapping/scraper.py')
        directory_exists = os.path.isdir('web_scrapping')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
