import os
from appcraft.utils.template_abc import TemplateABC


class WebSocketsTemplate(TemplateABC):
    _status = TemplateABC.AvailableStatus.inactive

    @property
    def description(self):
        return """
WebSockets Template provides resources for implementing real-time \
communication in applications using WebSockets. It includes configuration \
for WebSocket servers, client-side scripts, and message handling.
"""

    @classmethod
    def is_installed(cls):
        file_exists = os.path.isfile('websockets/server.py')
        directory_exists = os.path.isdir('websockets')

        return file_exists and directory_exists

    @classmethod
    def install(cls):
        pass

    @classmethod
    def uninstall(cls):
        pass
