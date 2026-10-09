from application.use_cases.app.get import GetAppUseCase
from infrastructure.app.adapter import AppAdapter
from infrastructure.core.runner import Runner
from presentation.cli.app import AppCLIPresentation


class App(Runner):
    @Runner.runner
    def show_informations(self):
        app_adapter = AppAdapter()
        app_use_case = GetAppUseCase(app_provider=app_adapter)
        presentation = AppCLIPresentation(app_use_case=app_use_case)
        presentation.show_informations()
