from application.ports.app import AppPort
from domain.models.app import App
from infrastructure.app.manager import AppManager


class AppAdapter(AppPort):
    def __init__(self):
        self._manager = AppManager()

    def get(self) -> App:
        return App(
            name=self._manager.name,
            version=self._manager.version,
            environment=self._manager.environment,
            debug_mode=self._manager.debug_mode,
        )
