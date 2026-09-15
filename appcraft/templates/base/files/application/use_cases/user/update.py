from application.mappers.update import UpdateMapper
from application.mappers.user import UserMapper
from application.repositories.user import UserRepository
from application.schemas.input.user import UserUpdateSchema
from application.schemas.output.user import UserOutSchema
from application.use_cases import UpdateUseCase
from domain.models.exceptions import ModelNotFoundError
from domain.models.exceptions.user_model_not_found import (
    UserModelNotFoundError,
)
from domain.models.user import User


class UpdateUserUseCase(UpdateUseCase[UserUpdateSchema, UserOutSchema]):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input_data: UserUpdateSchema) -> UserOutSchema:
        update = UpdateMapper.from_schema(User, input_data)

        try:
            user = self.repository.update_by_id(
                id=update.keys,
                changes=update.changes,
            )
        except ModelNotFoundError:
            raise UserModelNotFoundError

        return UserMapper.to_schema(user)
