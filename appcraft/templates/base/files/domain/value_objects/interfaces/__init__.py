from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ValueObjectInterface(ABC, Generic[T]):
    value: T
    _value = T

    @abstractmethod
    def __init__(self, value: T) -> None:
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: T):
        if self.is_valid(value):
            self._value = value

    @classmethod
    @abstractmethod
    def is_valid(value: T) -> bool:
        pass
