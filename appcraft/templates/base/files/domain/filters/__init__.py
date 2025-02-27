from typing import Any, List, Union

from domain.filters.base import FilterBase


class MinFilter(FilterBase[int]):
    pass


class MaxFilter(FilterBase[int]):
    pass


class EqualFilter(FilterBase[Union[str, int]]):
    pass


class InFilter(FilterBase[List[Any]]):
    pass


class LikeFilter(FilterBase[str]):
    pass
