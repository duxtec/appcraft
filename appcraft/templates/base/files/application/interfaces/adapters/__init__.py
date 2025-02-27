from abc import ABC, abstractmethod
from typing import List, Type

from domain.filters.interface import FilterInterface
from domain.types.model import ModelType


class AdapterInterface(ABC):
    pass


class ReaderAdapterInterface(AdapterInterface, ABC):
    @abstractmethod
    def get(
        self, model: Type[ModelType], filters: List[FilterInterface] = []
    ) -> List[ModelType]:
        pass


class WriterAdapterInterface(AdapterInterface, ABC):
    @abstractmethod
    def create(self, model: Type[ModelType], entity: ModelType) -> ModelType:
        pass

    @abstractmethod
    def update(
        self, model: Type[ModelType], id: int, entity: ModelType
    ) -> ModelType:
        pass

    @abstractmethod
    def delete(self, model: Type[ModelType], id: int) -> None:
        pass


class ReaderWriterAdapterInterface(
    ReaderAdapterInterface, WriterAdapterInterface, AdapterInterface, ABC
):
    pass
