import shutil
from typing import Any

from application.use_cases.database.list.columns import ListColumnsUseCase
from application.use_cases.database.list.tables import ListTablesUseCase
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class DatabaseCLIPresentation:
    class Printer(ComponentPrinter):
        domain = "database"

        @classmethod
        def print_title(cls):
            cls.title("Tables of database")

        @classmethod
        def show_table(cls, table: str, columns: list[Any]):
            cls.title("Table", end=": ")
            cls.success(table)
            for column in columns:
                cls.info(column["name"], end=": ")
                cls.warning(column["type"])

    def __init__(
        self,
        list_table_uc: ListTablesUseCase,
        list_columns_uc: ListColumnsUseCase,
    ) -> None:
        self.list_table_uc = list_table_uc
        self.list_columns_uc = list_columns_uc

    def show_tables(self):
        tables = self.list_table_uc.execute()
        h_line = '_' * shutil.get_terminal_size().columns
        self.Printer.print_title()
        for table in tables:
            self.Printer.warning(h_line)
            columns = self.list_columns_uc.execute(table)
            self.Printer.show_table(table, columns)
        self.Printer.warning(h_line)

    def show_columns(self, table: str):
        h_line = '_' * shutil.get_terminal_size().columns
        self.Printer.warning(h_line)
        columns = self.list_columns_uc.execute(table)
        self.Printer.show_table(table, columns)
        self.Printer.warning(h_line)
