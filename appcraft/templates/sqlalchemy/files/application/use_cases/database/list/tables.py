from application.use_cases import UseCase
from infrastructure.database.sqlalchemy.adapter import SQLAlchemyAdapter


class ListTablesUseCase(UseCase[None, list[str]]):
    def __init__(self, adapter: SQLAlchemyAdapter):
        self.adapter = adapter

    def execute(self, input_data: None = None) -> list[str]:
        try:
            return self.adapter.get_tables()
        except Exception as e:
            raise Exception(
                f"An error occurred while fetching tables: {str(e)}"
            )
