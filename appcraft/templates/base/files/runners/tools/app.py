from application.services.app_service import AppService
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.memory.adapters.app_adapter import AppAdapter
from presentation.cli.app import AppCLIPresentation


class App(AppRunnerInterface):
    @AppRunnerInterface.runner
    def show_informations(self):
        app_adapter = AppAdapter()
        app_service = AppService(app_adapter=app_adapter)
        presentation = AppCLIPresentation(app_service=app_service)
        presentation.show_informations()
