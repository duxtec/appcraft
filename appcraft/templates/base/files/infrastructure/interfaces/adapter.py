from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from domain.filters.interface import FilterInterface
from domain.models.interfaces import ModelInterface

T = TypeVar("T")


class AdapterInterface(ABC):
    @abstractmethod
    def get(
        self, model: Generic[T], filters: List[FilterInterface] = []
    ) -> List[ModelInterface]:
        pass

    @abstractmethod
    def create(self, model: Generic[T], entity: Generic[T]) -> Generic[T]:
        pass

    @abstractmethod
    def update(
        self, model: Generic[T], id: int, entity: Generic[T]
    ) -> Generic[T]:
        pass

    @abstractmethod
    def delete(self, model: Generic[T], id: int) -> None:
        pass
