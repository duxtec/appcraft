from infrastructure.adapters.sql_adapter import SqlAdapter


class DatabaseService:
    def __init__(self, adapter: SqlAdapter):
        self.adapter = adapter

    def list_tables(self):
        try:
            tables = self.adapter.get_tables()
            return tables
        except Exception as e:
            raise Exception(
                f"An error occurred while fetching tables: {str(e)}"
            )

    def list_columns(self, table_name):
        try:
            columns = self.adapter.get_columns(table_name)
            return columns
        except Exception as e:
            raise Exception(
                f"\
An error occurred while fetching columns from {table_name}: {str(e)}"
            )
