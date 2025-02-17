import os
from appcraft.utils.template_abc import TemplateABC


class LocaleTemplate(TemplateABC):
    @property
    def description(self):
        return """
Locale Template provides a structured way to manage multiple languages in \
your application. It includes pre-configured localization files, making it \
easier to handle translations and internationalization.
"""

    @classmethod
    def is_installed(cls):
        directory_exists = os.path.isdir('infrastructure/framework/appcraft')

        return directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
