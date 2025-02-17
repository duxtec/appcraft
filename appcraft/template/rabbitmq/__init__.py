import os
from appcraft.utils.template_abc import TemplateABC


class RabbitMQTemplate(TemplateABC):
    @property
    def description(self):
        return """
RabbitMQ Template sets up the environment for RabbitMQ message broker \
integration. It includes configuration files for connecting to RabbitMQ \
and managing message queues.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('rabbitmq/config.yaml')
        directory_exists = os.path.isdir('rabbitmq')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
