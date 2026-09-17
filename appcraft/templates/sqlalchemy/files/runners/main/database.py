from application.use_cases.database.list.columns import ListColumnsUseCase
from application.use_cases.database.list.tables import ListTablesUseCase
from infrastructure.database.sqlalchemy.adapter import get_sqlalchemy_adapter
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.database import DatabaseCLIPresentation


class Database(Runner):
    @Runner.runner
    def show_tables(self):
        adapter = get_sqlalchemy_adapter()
        list_tables_uc = ListTablesUseCase(adapter)
        list_columns_uc = ListColumnsUseCase(adapter)
        DatabaseCLIPresentation(
            list_table_uc=list_tables_uc,
            list_columns_uc=list_columns_uc,
        ).show_tables()

    @Runner.runner
    def show_columns(self, table: str | None = None):
        adapter = get_sqlalchemy_adapter()
        list_tables_uc = ListTablesUseCase(adapter)
        list_columns_uc = ListColumnsUseCase(adapter)
        presentation = DatabaseCLIPresentation(
            list_table_uc=list_tables_uc,
            list_columns_uc=list_columns_uc,
        )
        if table:
            presentation.show_columns(table)
        else:
            presentation.show_tables()
