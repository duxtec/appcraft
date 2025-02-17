import os
from appcraft.utils.template_abc import TemplateABC


class LogsTemplate(TemplateABC):
    @property
    def description(self):
        return """
Logs Template sets up logging configurations for the application. \
It provides log rotation, logging levels, and outputs for error tracking, \
ensuring that all application logs are captured and stored effectively.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('logs/log_config.yaml')
        directory_exists = os.path.isdir('logs')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
