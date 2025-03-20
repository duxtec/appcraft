from typing import List

from application.dtos.user_dto import UserDTO
from application.mappers.user_mapper import UserMapper
from application.services.interfaces import ServiceInterface
from domain.filters import EqualFilter
from domain.filters.interface import FilterInterface
from domain.interfaces.repositories.user_repository import (
    UserRepositoryInterface,
)
from domain.models.exceptions.user_model_not_found import (
    UserModelNotFoundError,
)
from domain.models.user import User


class UserService(ServiceInterface):
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def get(self, filters: List[FilterInterface] = []) -> List[UserDTO]:
        users = self.user_repository.get(filters)
        users_dto: List[UserDTO] = []
        for user in users:
            users_dto.append(UserMapper.to_dto(user))

        return users_dto

    def create(self, username: str) -> UserDTO:
        user = User(id=None, username=username)
        user = self.user_repository.create(user)
        user_dto = UserMapper.to_dto(user)
        return user_dto

    def update(self, id: int, username: str) -> UserDTO:
        filters: List[FilterInterface] = [EqualFilter(User.id, id)]
        user = self.user_repository.get(filters)
        if len(user) == 0:
            raise UserModelNotFoundError()

        user = user[0]
        user.username = username
        user = self.user_repository.update(user)
        user_dto = UserMapper.to_dto(user)
        return user_dto

    def delete(self, id: int) -> None:
        filters: List[FilterInterface] = [EqualFilter(User.id, id)]
        user = self.user_repository.get(filters)[0]
        self.user_repository.delete(user)
