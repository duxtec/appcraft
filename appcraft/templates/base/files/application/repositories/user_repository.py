from typing import List

from application.interfaces.adapters.database_adapter import (
    DatabaseAdapterInterface,
)
from domain.filters.interface import FilterInterface
from domain.interfaces.repositories.user_repository import (
    UserRepositoryInterface,
)
from domain.models.exceptions import ModelNotFoundError
from domain.models.exceptions.user_model_not_found import (
    UserModelNotFoundError,
)
from domain.models.user import User


class UserRepository(UserRepositoryInterface):
    def __init__(self, adapter: DatabaseAdapterInterface) -> None:
        self.adapter = adapter

    def get(self, filters: List[FilterInterface]) -> List[User]:
        users = self.adapter.get(User, filters)
        if len(users) == 0:
            raise UserModelNotFoundError()

        return users

    def create(self, user: User) -> User:
        try:
            return self.adapter.create(User, user)
        except ModelNotFoundError:
            raise UserModelNotFoundError()

    def update(self, user: User) -> User:
        try:
            return self.adapter.update(User, user.id, user)
        except ModelNotFoundError:
            raise UserModelNotFoundError()

    def delete(self, user: User) -> None:
        try:
            return self.adapter.delete(User, user.id)
        except ModelNotFoundError:
            raise UserModelNotFoundError()
