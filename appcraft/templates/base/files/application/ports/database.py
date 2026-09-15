from abc import ABC, abstractmethod
from typing import Sequence, Type

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports import Port
from domain.filters.interface import FilterInterface
from domain.models import NewModel
from domain.types.model import TModel
from domain.value_objects.id import Id


class DatabaseReaderPort(Port, ABC):
    @abstractmethod
    def get(
        self, model: Type[TModel], filters: Sequence[FilterInterface] = []
    ) -> list[TModel]:
        pass


class DatabaseWriterPort(Port, ABC):
    @abstractmethod
    def create(self, model: type[TModel], entity: NewModel) -> TModel:
        pass

    @abstractmethod
    def update(
        self,
        model: type[TModel],
        entity: TModel,
    ) -> TModel:
        pass

    @abstractmethod
    def update_where(
        self,
        model: type[TModel],
        filters: list[FilterInterface],
        changes: Changes,
    ) -> int:
        pass

    @abstractmethod
    def update_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
        changes: Changes,
    ) -> TModel: ...

    @abstractmethod
    def delete(self, model: type[TModel], entity: TModel) -> None:
        pass

    @abstractmethod
    def delete_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
    ) -> None:
        pass

    @abstractmethod
    def delete_where(
        self,
        model: type[TModel],
        filters: list[FilterInterface],
    ) -> int:
        pass


class DatabasePort(
    DatabaseReaderPort,
    DatabaseWriterPort,
    ABC,
):
    pass
