from typing import Dict, List, Type

from application.interfaces.adapters.database_adapter import (
    DatabaseAdapterInterface,
)
from domain.filters import (
    EqualFilter,
    InFilter,
    LikeFilter,
    MaxFilter,
    MinFilter,
)
from domain.filters.interface import FilterInterface
from domain.models.exceptions import ModelNotFoundError
from domain.models.interfaces import ModelInterface


class MemoryAdapter(DatabaseAdapterInterface):
    def __init__(self):
        self._storage: StorageMemory = StorageMemory()
        self._filter: FilterMemory = FilterMemory()

    def get(
        self, model: Type[ModelInterface], filters: List[FilterInterface] = []
    ) -> List[ModelInterface]:
        model_storage = self._storage.get_model_storage(model)
        result = model_storage.data.copy()
        for filter in filters:
            result = self._filter.apply_filter(result, filter)

        return list(result.values())

    def create(
        self, model: Type[ModelInterface], entity: ModelInterface
    ) -> ModelInterface:
        if not isinstance(entity, model):
            raise TypeError("The entity is not of the expected model type.")

        model_storage = self._storage.get_model_storage(model)
        current_id = model_storage.last_id + 1
        entity.id = current_id
        model_storage.save(entity)
        model_storage.increment_last_id()
        return entity

    def update(
        self, model: Type[ModelInterface], id: int, entity: ModelInterface
    ) -> ModelInterface:
        model_storage = self._storage.get_model_storage(model)
        if id not in model_storage.data:
            raise ModelNotFoundError(model)

        if entity.id is not None and id != entity.id:
            raise ValueError(
                f"\
ID to be updated ({id}) is different from the entity ID ({entity.id})"
            )

        model_storage.save(entity)

        return entity

    def delete(self, model: Type[ModelInterface], id: int) -> None:
        model_storage = self._storage.get_model_storage(model)

        if id not in model_storage.data:
            raise ModelNotFoundError(model)

        del model_storage.data[id]


class FilterMemory:
    @classmethod
    def apply_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: FilterInterface
    ) -> Dict[str, ModelInterface]:
        filter_actions = {
            MinFilter.__name__: cls.apply_min_filter,
            MaxFilter.__name__: cls.apply_max_filter,
            EqualFilter.__name__: cls.apply_equal_filter,
            InFilter.__name__: cls.apply_in_filter,
            LikeFilter.__name__: cls.apply_like_filter,
        }

        filter_name = filter.__class__.__name__

        filter_action = filter_actions.get(filter_name, None)

        if filter_action:
            return filter_action(model_storage, filter)
        else:
            raise TypeError(f"Unsupported filter type: {filter_name}")

    @classmethod
    def apply_min_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: MinFilter
    ) -> Dict[str, ModelInterface]:
        return {
            key: item
            for key, item in model_storage.items()
            if (value := getattr(item, filter.property, None)) is not None
            and value >= filter.value
        }

    @classmethod
    def apply_max_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: MaxFilter
    ) -> Dict[str, ModelInterface]:
        return {
            key: item
            for key, item in model_storage.items()
            if (value := getattr(item, filter.property, None)) is not None
            and value <= filter.value
        }

    @classmethod
    def apply_equal_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: EqualFilter
    ) -> Dict[str, ModelInterface]:
        return {
            key: item
            for key, item in model_storage.items()
            if getattr(item, filter.property, None) == filter.value
        }

    @classmethod
    def apply_in_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: InFilter
    ) -> Dict[str, ModelInterface]:
        return {
            key: item
            for key, item in model_storage.items()
            if getattr(item, filter.property, None) in filter.value
        }

    @classmethod
    def apply_like_filter(
        cls, model_storage: Dict[str, ModelInterface], filter: LikeFilter
    ) -> Dict[str, ModelInterface]:
        return {
            key: item
            for key, item in model_storage.items()
            if filter.value in getattr(item, filter.property, "")
        }


class ModelStorageMemory:
    def __init__(self, model: Type[ModelInterface]) -> None:
        self.model = model
        self._last_id = 0
        self._data = {}

    @property
    def last_id(self):
        return self._last_id

    def increment_last_id(self):
        self._last_id += 1

    @property
    def data(self):
        return self._data

    def save(self, model: ModelInterface):
        if not isinstance(model, self.model):
            raise TypeError("The entity is not of the expected model type.")

        self.data[model.id] = model


class StorageMemory:
    def __init__(self) -> None:
        self.model_storages = {}

    def create_model_storage(self, model: Type[ModelInterface]):
        model_name = model.__name__
        if model_name not in self.model_storages:
            self.model_storages[model_name] = ModelStorageMemory(model)

    def get_model_storage(
        self, model: Type[ModelInterface]
    ) -> ModelStorageMemory:
        model_name = model.__name__
        self.create_model_storage(model)
        return self.model_storages[model_name]
