from application.mappers.user import UserMapper
from application.repositories.user import UserRepository
from application.schemas.input.user import UserInSchema
from application.schemas.output.user import UserOutSchema
from application.use_cases import CreateUseCase
from domain.models.user import NewUser


class CreateUserUseCase(CreateUseCase[UserInSchema, UserOutSchema]):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input_data: UserInSchema) -> UserOutSchema:
        new_user = NewUser(**input_data.model_dump())
        user = self.repository.create(new_user)
        return UserMapper.to_schema(user)
