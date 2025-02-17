import os
from appcraft.utils.template_abc import TemplateABC


class GraphQLTemplate(TemplateABC):
    @property
    def description(self):
        return """
GraphQL Template provides the necessary setup for creating and managing \
GraphQL APIs. It includes the necessary configuration files, schema \
definitions, and resolvers to help you build a flexible and efficient \
GraphQL API layer.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('graphql/schema.graphql')
        directory_exists = os.path.isdir('graphql')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
