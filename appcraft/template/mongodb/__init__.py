import os
from appcraft.utils.template_abc import TemplateABC


class MongoDBTemplate(TemplateABC):
    @property
    def description(self):
        return """
MongoDB Template sets up the environment for MongoDB database integration. \
It includes configuration files for connecting to MongoDB, as well as \
predefined models and schemas for data storage and retrieval.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('mongodb/config.py')
        directory_exists = os.path.isdir('mongodb')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
