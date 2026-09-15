from abc import ABC, abstractmethod
from typing import TypeVar

from domain.models.core.field import Field

T = TypeVar("T", covariant=True)


class FilterInterface(ABC):
    @abstractmethod
    def __init__(
        self,
        model_property: Field[T],
        value: T,
        include: bool | None = None,
        not_param: bool | None = None,
    ):
        pass
