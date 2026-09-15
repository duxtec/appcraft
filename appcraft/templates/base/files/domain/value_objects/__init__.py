from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ValueType = TypeVar("ValueType")


class ValueObject(Generic[ValueType], ABC):
    _value: ValueType

    @abstractmethod
    def __init__(self, value: ValueType | str) -> None:
        pass

    @property
    @abstractmethod
    def value(self) -> ValueType:
        pass

    @classmethod
    @abstractmethod
    def is_valid(cls, value: ValueType) -> bool:
        pass
