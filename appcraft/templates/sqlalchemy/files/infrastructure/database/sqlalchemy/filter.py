from typing import Any, Callable, TypeVar, cast

from sqlalchemy.orm import Query

from domain.filters import (
    EqualFilter,
    InFilter,
    LikeFilter,
    MaxFilter,
    MinFilter,
)
from domain.filters.interface import FilterInterface
from domain.value_objects.base import ValueObjectBase

TQuery = TypeVar("TQuery")


class FilterSQLAlchemy:
    @staticmethod
    def _unwrap_value(value: Any) -> Any:
        """Domain value objects (e.g. Id subclasses) aren't a type the
        DBAPI driver knows how to bind — unwrap to the primitive it holds.
        """
        if isinstance(value, ValueObjectBase):
            return cast(Any, value).value
        return value

    @classmethod
    def apply_filter(
        cls,
        query: Query[TQuery],
        orm_model: Any,
        filter: FilterInterface,
    ) -> Query[TQuery]:
        filter_actions: dict[str, Callable[..., Query[TQuery]]] = {
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

        return filter_action(query, orm_model, filter)  # type: ignore

    @classmethod
    def apply_min_filter(
        cls, query: Query[TQuery], orm_model: Any, filter: MinFilter
    ) -> Query[TQuery]:
        column = getattr(orm_model, filter.property)
        return query.filter(column >= cls._unwrap_value(filter.value))

    @classmethod
    def apply_max_filter(
        cls, query: Query[TQuery], orm_model: Any, filter: MaxFilter
    ) -> Query[TQuery]:
        column = getattr(orm_model, filter.property)
        return query.filter(column <= cls._unwrap_value(filter.value))

    @classmethod
    def apply_equal_filter(
        cls, query: Query[TQuery], orm_model: Any, filter: EqualFilter[Any]
    ) -> Query[TQuery]:
        column = getattr(orm_model, filter.property)
        return query.filter(column == cls._unwrap_value(filter.value))

    @classmethod
    def apply_in_filter(
        cls, query: Query[TQuery], orm_model: Any, filter: InFilter
    ) -> Query[TQuery]:
        column = getattr(orm_model, filter.property)
        values = [cls._unwrap_value(value) for value in filter.value]
        return query.filter(column.in_(values))

    @classmethod
    def apply_like_filter(
        cls, query: Query[TQuery], orm_model: Any, filter: LikeFilter
    ) -> Query[TQuery]:
        column = getattr(orm_model, filter.property)
        return query.filter(
            column.like(f"%{cls._unwrap_value(filter.value)}%")
        )
