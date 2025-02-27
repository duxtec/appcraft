from abc import abstractmethod
from typing import List

from domain.filters.interface import FilterInterface
from domain.interfaces.repositories import RepositoryInterface
from domain.models.user import User


class UserRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def get(self, filters: List[FilterInterface]) -> List[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
