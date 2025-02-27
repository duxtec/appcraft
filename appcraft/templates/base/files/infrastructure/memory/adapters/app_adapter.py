from application.interfaces.adapters.app_adapter import AppAdapterInterface
from domain.models.app import App
from infrastructure.framework.appcraft.core.app_manager import AppManager


class AppAdapter(AppAdapterInterface):
    def __init__(self):
        self.manager = AppManager()

    def get(self) -> App:
        app = App(
            name=self.manager.name,
            version=self.manager.version,
            environment=self.manager.environment,
            debug_mode=self.manager.debug_mode,
        )

        return app
