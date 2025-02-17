import os
from appcraft.utils.template_abc import TemplateABC


class DockerTemplate(TemplateABC):
    @property
    def description(self):
        return """
Docker Template provides resources for containerizing the application using \
Docker. It includes a pre-configured Dockerfile, ensuring that the \
application can be easily built and deployed in a containerized environment.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('docker/Dockerfile')
        directory_exists = os.path.isdir('docker')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        super().install()

    @classmethod
    def uninstall(cls):
        pass
