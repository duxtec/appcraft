from infrastructure.framework.appcraft.core.app_runner import AppRunner
from presentation.cli.app_cli_presentation import AppCLIPresentation


class App(AppRunner):
    @AppRunner.runner
    def start(self):
        AppCLIPresentation().start()

    def non_runner1(self):
        # This method does not show in the runner.
        pass
