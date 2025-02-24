from abc import ABC, abstractmethod
from typing import List

from domain.filters import FilterInterface
from domain.models.user import User


class UserRepositoryInterface(ABC):
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
