from abc import ABC, abstractmethod
from typing import List, TypeVar

from domain.filters.interface import FilterInterface
from domain.models.interfaces import ModelInterface

T = TypeVar("T", bound=ModelInterface)


class AdapterInterface(ABC):
    @abstractmethod
    def get(
        self, model: type[T], filters: List[FilterInterface] = []
    ) -> List[T]:
        pass

    @abstractmethod
    def create(self, model: type[T], entity: T) -> T:
        pass

    @abstractmethod
    def update(self, model: type[T], id: int, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, model: type[T], id: int) -> None:
        pass
