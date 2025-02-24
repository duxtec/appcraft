from domain.models.app import App
from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.memory.adapters.interfaces.app_adapter_interface import (
    AppAdapterInterface,
)


class AppAdapter(AppAdapterInterface):
    def __init__(self):
        self.manager = AppManager()

    def get_app(self) -> App:
        app = App(
            name=self.manager.name(),
            version=self.manager.version(),
            environment=self.manager.environment(),
            debug_mode=self.manager.debug_mode(),
        )

        return app
