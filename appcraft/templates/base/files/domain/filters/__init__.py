from typing import Any, SupportsInt, TypeVar

from domain.filters.base import FilterBase

T = TypeVar("T", str, SupportsInt)


class MinFilter(FilterBase[SupportsInt]):
    pass


class MaxFilter(FilterBase[SupportsInt]):
    pass


class EqualFilter(FilterBase[T]):
    pass


class InFilter(FilterBase[list[Any]]):
    pass


class LikeFilter(FilterBase[str]):
    pass
