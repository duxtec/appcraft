from infrastructure.framework.appcraft.core.app_runner import AppRunner
from presentation.cli.app_cli_presentation import AppCLIPresentation


class App(AppRunner):
    @AppRunner.runner
    def show_informations(self):
        AppCLIPresentation().show_informations()
