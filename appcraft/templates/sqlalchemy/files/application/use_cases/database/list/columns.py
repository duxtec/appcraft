from typing import Any

from application.use_cases import UseCase
from infrastructure.database.sqlalchemy.adapter import SQLAlchemyAdapter


class ListColumnsUseCase(UseCase[str, list[Any]]):
    def __init__(self, adapter: SQLAlchemyAdapter):
        self.adapter = adapter

    def execute(self, input_data: str) -> list[Any]:
        try:
            return self.adapter.get_columns(input_data)
        except Exception as e:
            raise Exception(
                f"An error occurred while fetching "
                f"columns from {input_data}: {str(e)}"
            )
