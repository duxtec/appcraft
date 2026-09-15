from application.use_cases.app.get import GetAppUseCase
from infrastructure.framework.appcraft.app.provider import AppProvider
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.app import AppCLIPresentation


class AppRunner(Runner):
    @Runner.runner
    def start(self):
        app_adapter = AppProvider()
        app_service = GetAppUseCase(app_provider=app_adapter)
        presentation = AppCLIPresentation(app_use_case=app_service)
        presentation.start()

    def non_runner1(self):
        # This method does not show in the runner.
        pass
