import shutil
from typing import List
from infrastructure.adapters.sql_adapter import SqlAdapter
from application.services.database_service import DatabaseService
from infrastructure.framework.appcraft.utils.component_printer \
    import ComponentPrinter


class DatabaseCLIPresentation():
    class Printer(ComponentPrinter):
        domain = "database"

        @classmethod
        def print_title(cls):
            cls.title("Tables of database")

        @classmethod
        def show_table(cls, table: str, columns: List):
            cls.title("Table", end=": ")
            cls.success(table)
            for column in columns:
                cls.info(column["name"], end=": ")
                cls.warning(column["type"])

    def show_tables(self):
        adapter = SqlAdapter()
        service = DatabaseService(adapter)
        tables = service.list_tables()
        h_line = '_' * shutil.get_terminal_size().columns
        self.Printer.print_title()
        for table in tables:
            self.Printer.warning(h_line)
            columns = service.list_columns(table)
            self.Printer.show_table(table, columns)
        self.Printer.warning(h_line)
