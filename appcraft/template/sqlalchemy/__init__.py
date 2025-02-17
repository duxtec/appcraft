import os
from appcraft.utils.template_abc import TemplateABC


class SQLAlchemyTemplate(TemplateABC):
    @property
    def description(self):
        return """
SQLAlchemy Template provides a setup for integrating the SQLAlchemy ORM with \
your application. It includes configuration files for database connection, as \
well as predefined models for interacting with relational databases.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('sqlalchemy/models.py')
        directory_exists = os.path.isdir('sqlalchemy')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
