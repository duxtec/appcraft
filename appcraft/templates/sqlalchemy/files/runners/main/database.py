from infrastructure.framework.appcraft.core.app_runner import AppRunner
from presentation.cli.database_cli_presentation import DatabaseCLIPresentation


class Database(AppRunner):
    @AppRunner.runner
    def show_tables(self):
        DatabaseCLIPresentation().show_tables()
