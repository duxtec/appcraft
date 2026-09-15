from application.use_cases.app.get import GetAppUseCase
from infrastructure.framework.appcraft.app.provider import AppProvider
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.app import AppCLIPresentation


class App(Runner):
    @Runner.runner
    def show_informations(self):
        app_adapter = AppProvider()
        app_use_case = GetAppUseCase(app_provider=app_adapter)
        presentation = AppCLIPresentation(app_use_case=app_use_case)
        presentation.show_informations()
