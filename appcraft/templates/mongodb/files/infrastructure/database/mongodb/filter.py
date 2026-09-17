import re
from typing import Any, Callable, Sequence, cast

from domain.filters import (
    EqualFilter,
    InFilter,
    LikeFilter,
    MaxFilter,
    MinFilter,
)
from domain.filters.base import FilterBase
from domain.filters.interface import FilterInterface
from domain.value_objects.base import ValueObjectBase


class FilterMongoDB:
    @staticmethod
    def _unwrap_value(value: Any) -> Any:
        """Domain value objects (e.g. Id subclasses) aren't BSON-native —
        unwrap to the primitive it holds.
        """
        if isinstance(value, ValueObjectBase):
            return cast(Any, value).value
        return value

    @classmethod
    def _property_name(cls, filter: FilterBase[Any]) -> str:
        # The domain's `id` field is stored as Mongo's own `_id`.
        return "_id" if filter.property == "id" else filter.property

    @classmethod
    def build_query(
        cls, filters: Sequence[FilterInterface]
    ) -> dict[str, Any]:
        query: dict[str, Any] = {}
        for filter in filters:
            query.update(cls._to_clause(filter))
        return query

    @classmethod
    def _to_clause(cls, filter: FilterInterface) -> dict[str, Any]:
        filter_actions: dict[str, Callable[[Any], dict[str, Any]]] = {
            MinFilter.__name__: cls._min_clause,
            MaxFilter.__name__: cls._max_clause,
            EqualFilter.__name__: cls._equal_clause,
            InFilter.__name__: cls._in_clause,
            LikeFilter.__name__: cls._like_clause,
        }

        filter_name = filter.__class__.__name__
        filter_action = filter_actions.get(filter_name, None)

        if not filter_action:
            raise TypeError(f"Unsupported filter type: {filter_name}")

        return filter_action(filter)

    @classmethod
    def _min_clause(cls, filter: MinFilter) -> dict[str, Any]:
        return {
            cls._property_name(filter): {
                "$gte": cls._unwrap_value(filter.value)
            }
        }

    @classmethod
    def _max_clause(cls, filter: MaxFilter) -> dict[str, Any]:
        return {
            cls._property_name(filter): {
                "$lte": cls._unwrap_value(filter.value)
            }
        }

    @classmethod
    def _equal_clause(cls, filter: EqualFilter[Any]) -> dict[str, Any]:
        return {cls._property_name(filter): cls._unwrap_value(filter.value)}

    @classmethod
    def _in_clause(cls, filter: InFilter) -> dict[str, Any]:
        values = [cls._unwrap_value(value) for value in filter.value]
        return {cls._property_name(filter): {"$in": values}}

    @classmethod
    def _like_clause(cls, filter: LikeFilter) -> dict[str, Any]:
        pattern = re.escape(str(cls._unwrap_value(filter.value)))
        return {
            cls._property_name(filter): {
                "$regex": pattern,
                "$options": "i",
            }
        }
