from typing import Any, Callable

from domain.filters import (
    EqualFilter,
    InFilter,
    LikeFilter,
    MaxFilter,
    MinFilter,
)
from domain.filters.interface import FilterInterface
from domain.types.model import TModel
from infrastructure.memory.storage import StorageKey


class FilterMemory:
    @classmethod
    def apply_filter(
        cls,
        model_storage: dict[StorageKey, TModel],
        filter: FilterInterface,
    ) -> dict[StorageKey, TModel]:
        filter_actions: dict[str, Callable[..., Any]] = {
            MinFilter.__name__: cls.apply_min_filter,
            MaxFilter.__name__: cls.apply_max_filter,
            EqualFilter.__name__: cls.apply_equal_filter,
            InFilter.__name__: cls.apply_in_filter,
            LikeFilter.__name__: cls.apply_like_filter,
        }

        filter_name = filter.__class__.__name__

        filter_action = filter_actions.get(filter_name, None)

        if not filter_action:
            raise TypeError(f"Unsupported filter type: {filter_name}")

        return filter_action(model_storage, filter)  # type: ignore

    @classmethod
    def apply_min_filter(
        cls, model_storage: dict[StorageKey, TModel], filter: MinFilter
    ) -> dict[StorageKey, TModel]:
        return {
            key: item
            for key, item in model_storage.items()
            if (value := getattr(item, filter.property, None)) is not None
            and value >= filter.value
        }

    @classmethod
    def apply_max_filter(
        cls, model_storage: dict[StorageKey, TModel], filter: MaxFilter
    ) -> dict[StorageKey, TModel]:
        return {
            key: item
            for key, item in model_storage.items()
            if (value := getattr(item, filter.property, None)) is not None
            and value <= filter.value
        }

    @classmethod
    def apply_equal_filter(
        cls, model_storage: dict[StorageKey, TModel], filter: EqualFilter[Any]
    ) -> dict[StorageKey, TModel]:
        return {
            key: item
            for key, item in model_storage.items()
            if getattr(item, filter.property, None) == filter.value
        }

    @classmethod
    def apply_in_filter(
        cls, model_storage: dict[StorageKey, TModel], filter: InFilter
    ) -> dict[StorageKey, TModel]:
        return {
            key: item
            for key, item in model_storage.items()
            if getattr(item, filter.property, None) in filter.value
        }

    @classmethod
    def apply_like_filter(
        cls, model_storage: dict[StorageKey, TModel], filter: LikeFilter
    ) -> dict[StorageKey, TModel]:
        return {
            key: item
            for key, item in model_storage.items()
            if filter.value in getattr(item, filter.property, "")
        }
