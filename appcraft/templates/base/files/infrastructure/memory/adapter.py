from typing import Sequence, Type

from application.core.changes import Changes
from application.core.keys import Keys
from application.ports.database import DatabasePort
from domain.filters.interface import FilterInterface
from domain.models import NewModel
from domain.models.exceptions import ModelNotFoundError
from domain.types.model import TModel
from domain.value_objects.id import Id
from infrastructure.memory.filter import FilterMemory
from infrastructure.memory.seeder import MemoryAdapterSeeder
from infrastructure.memory.storage import StorageMemory


class MemoryAdapter(DatabasePort):
    def __init__(self):
        self._storage: StorageMemory = StorageMemory()
        self._filter: FilterMemory = FilterMemory()

        MemoryAdapterSeeder(self).seed()

    def get(
        self,
        model: Type[TModel],
        filters: Sequence[FilterInterface] | None = None,
    ) -> list[TModel]:
        model_storage = self._storage.get_model_storage(model)
        result = model_storage.data.copy()
        for filter in filters or []:
            result = self._filter.apply_filter(result, filter)

        return list(result.values())

    def create(self, model: Type[TModel], entity: NewModel) -> TModel:
        model_storage = self._storage.get_model_storage(model)

        if not isinstance(entity, model):
            current_id = model_storage.last_id + 1
            if model.id.type:
                current_id = model.id.type(current_id)
            entity = model(
                id=current_id,
                **entity.model_dump(),
            )

        model_storage.save(entity)
        model_storage.increment_last_id()
        return entity

    def update(
        self,
        model: Type[TModel],
        entity: TModel,
    ) -> TModel:
        model_storage = self._storage.get_model_storage(model)

        pks = model.primary_keys()

        stored = next(
            (
                item
                for item in model_storage.data.values()
                if all(
                    getattr(item, pk.name) == getattr(entity, pk.name)
                    for pk in pks
                )
            ),
            None,
        )

        if stored is None:
            raise ModelNotFoundError(model)

        key_values = tuple(getattr(stored, pk.name) for pk in pks)
        model_storage.data[key_values if len(pks) > 1 else key_values[0]] = (
            entity
        )
        return entity

    def update_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
        changes: Changes,
    ) -> TModel:
        model_storage = self._storage.get_model_storage(model)

        pks = model.primary_keys()

        if len(pks) == 1 and isinstance(id, Id):
            key = id.value

        if isinstance(id, Id):
            key = (id.value,)

        else:
            key = tuple(pk[1] for pk in id.items())

        entity = model_storage.data.get(key)

        if entity is None:
            raise ModelNotFoundError(model)

        for field, value in changes.items():
            setattr(entity, field.name, value)

        return entity

    def update_where(
        self,
        model: type[TModel],
        filters: Sequence[FilterInterface],
        changes: Changes,
    ) -> int:
        model_storage = self._storage.get_model_storage(model)
        data = model_storage.data

        updated = 0

        for filter in filters:
            data = FilterMemory.apply_filter(data, filter)

        for entity in data.values():
            for field, value in changes.items():
                setattr(entity, field.name, value)
            updated += 1

        return updated

    def delete(
        self,
        model: Type[TModel],
        entity: TModel,
    ) -> None:
        model_storage = self._storage.get_model_storage(model)

        pks = model.primary_keys()

        stored = next(
            (
                item
                for item in model_storage.data.values()
                if all(
                    getattr(item, pk.name) == getattr(entity, pk.name)
                    for pk in pks
                )
            ),
            None,
        )

        if stored is None:
            raise ModelNotFoundError(model)

        key_values = tuple(getattr(stored, pk.name) for pk in pks)

        del model_storage.data[key_values]

    def delete_by_id(
        self,
        model: type[TModel],
        id: Id | Keys,
    ) -> None:
        model_storage = self._storage.get_model_storage(model)

        pks = model.primary_keys()

        if len(pks) == 1 and isinstance(id, Id):
            key = id.value

        if isinstance(id, Id):
            key = (id.value,)

        else:
            key = tuple(pk[1] for pk in id.items())

        if key not in model_storage.data:
            raise ModelNotFoundError(model)

        del model_storage.data[key]

    def delete_where(
        self,
        model: Type[TModel],
        filters: list[FilterInterface] | None = None,
    ) -> int:
        model_storage = self._storage.get_model_storage(model)
        result = model_storage.data.copy()

        for filter in filters or []:
            result = self._filter.apply_filter(result, filter)

        if not result:
            return 0

        for key in result.keys():
            del model_storage.data[key]

        return len(result)
