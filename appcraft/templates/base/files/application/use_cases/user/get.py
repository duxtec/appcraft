from typing import Sequence

from application.mappers.user import UserMapper
from application.repositories.user import UserRepository
from application.schemas.output.user import UserOutSchema
from application.use_cases import ReadOneUseCase, ReadUseCase
from domain.filters import EqualFilter
from domain.filters.interface import FilterInterface
from domain.models.user import User, UserId


class ReadUserUseCase(ReadUseCase[UserOutSchema]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(
        self, input_data: Sequence[FilterInterface]
    ) -> list[UserOutSchema]:
        users = self.repository.get(filters=input_data)
        return [UserMapper.to_schema(user) for user in users]


class ReadOneUserUseCase(ReadOneUseCase[UserId, UserOutSchema]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, input_data: UserId) -> UserOutSchema:
        users = self.repository.get(
            filters=[EqualFilter(User.id, input_data)]
        )
        return UserMapper.to_schema(users[0])
