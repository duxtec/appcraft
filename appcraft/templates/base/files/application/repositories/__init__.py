from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports.database import DatabasePort
from domain.filters.interface import FilterInterface
from domain.types.model import TModel, TNewModel
from domain.value_objects.id import Id

ValueType = TypeVar("ValueType")


class Repository(
    ABC,
    Generic[TModel, TNewModel],
):
    adapter: DatabasePort
    model: type[TModel]
    new_model: type[TNewModel]

    @abstractmethod
    def get(
        self,
        filters: list[FilterInterface],
    ) -> list[TModel]:
        pass

    @abstractmethod
    def create(
        self,
        entity: TNewModel,
    ) -> TModel:
        pass

    @abstractmethod
    def update(
        self,
        entity: TModel,
    ) -> TModel: ...

    @abstractmethod
    def update_by_id(
        self,
        id: Id | Keys,
        changes: Changes,
    ) -> TModel: ...

    @abstractmethod
    def delete(
        self,
        entity: TModel,
    ) -> None: ...

    @abstractmethod
    def delete_by_id(
        self,
        id: Id | Keys,
    ) -> None: ...


class RepositoryBase(
    Repository[TModel, TNewModel],
):

    def get(
        self,
        filters: list[FilterInterface],
    ) -> list[TModel]:
        model = self.model
        result = self.adapter.get(model, filters)
        return result

    def create(
        self,
        entity: TNewModel,
    ) -> TModel: ...

    def update(
        self,
        entity: TModel,
    ) -> TModel:
        return self.adapter.update(self.model, entity)

    def update_by_id(
        self,
        id: Id | Keys,
        changes: Changes,
    ) -> TModel:
        return self.adapter.update_by_id(self.model, id, changes)

    def delete(
        self,
        entity: TModel,
    ) -> None:
        return self.adapter.delete(self.model, entity)

    def delete_by_id(
        self,
        id: Id | Keys,
    ) -> None:
        return self.adapter.delete_by_id(self.model, id)


class GenericRepository(
    RepositoryBase[TModel, TNewModel],
):
    def __init__(
        self,
        adapter: DatabasePort,
        model: type[TModel],
        new_model: type[TNewModel],
    ) -> None:
        self.adapter = adapter
        self.model = model
        self.new_model = new_model
