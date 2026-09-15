from application.repositories.user import UserRepository
from application.schemas.input.user import UserDeleteSchema
from application.use_cases import DeleteUseCase
from domain.models.exceptions import ModelNotFoundError
from domain.models.exceptions.user_model_not_found import (
    UserModelNotFoundError,
)
from domain.models.user import UserId


class DeleteUserUseCase(DeleteUseCase[UserDeleteSchema]):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input_data: UserDeleteSchema) -> None:

        id = UserId(input_data.id)

        try:
            return self.repository.delete_by_id(
                id=id,
            )
        except ModelNotFoundError:
            raise UserModelNotFoundError
