from typing import Any, Generic, Type

from domain.types.model import TModel

StorageKey = int | str | tuple[Any]


class ModelStorageMemory(Generic[TModel]):
    def __init__(self, model: Type[TModel], keys: list[str] = ["id"]) -> None:
        self.model = model
        self.keys = keys
        self._last_id = 0
        self._data: dict[StorageKey, TModel] = {}

    @property
    def last_id(self) -> int:
        return self._last_id

    def increment_last_id(self) -> None:
        self._last_id += 1

    @property
    def data(self) -> dict[StorageKey, TModel]:
        return self._data

    def _build_key(self, entity: TModel) -> StorageKey:
        key_values = tuple(getattr(entity, key) for key in self.keys)
        return key_values

    def save(self, entity: TModel) -> None:
        if not isinstance(entity, self.model):
            raise TypeError("The entity is not of the expected model type.")

        if getattr(entity, "id", None) is None:
            self._last_id += 1
            entity.id = self._last_id

        index = self._build_key(entity)
        self._data[index] = entity

    def remove(self, entity: TModel) -> None:
        index = self._build_key(entity)
        if index not in self._data:
            raise KeyError(f"Key {index} not found.")
        del self._data[index]


class StorageMemory:
    def __init__(self) -> None:
        self.model_storages: dict[str, ModelStorageMemory[Any]] = {}

    def create_model_storage(
        self,
        model: Type[TModel],
        keys: list[str] = ["id"],
    ) -> None:
        model_name = model.__name__
        if model_name not in self.model_storages:
            self.model_storages[model_name] = ModelStorageMemory(model, keys)

    def get_model_storage(
        self,
        model: Type[TModel],
        keys: list[str] = ["id"],
    ) -> ModelStorageMemory[TModel]:
        model_name = model.__name__
        self.create_model_storage(model, keys)
        return self.model_storages[model_name]
