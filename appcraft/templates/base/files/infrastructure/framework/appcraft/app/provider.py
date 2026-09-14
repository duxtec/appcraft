from application.providers.app import IAppProvider
from domain.models.app import App
from infrastructure.framework.appcraft.app.manager import AppManager


class AppProvider(IAppProvider):
    def __init__(self):
        self._manager = AppManager()

    def get(self) -> App:
        return App(
            name=self._manager.name,
            version=self._manager.version,
            environment=self._manager.environment,
            debug_mode=self._manager.debug_mode,
        )
