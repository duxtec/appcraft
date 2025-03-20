from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.value_objects.converters.type_conversor import (
    ValueObjectTypeConversor,
)
from domain.value_objects.interfaces import ValueObjectInterface

T = TypeVar("T")


class ValueObjectBase(ValueObjectInterface[T], Generic[T], ABC):
    _value: T

    def __init__(self, value: T | str) -> None:
        self.value = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T | str):
        if isinstance(value, str):
            value = ValueObjectTypeConversor[T](self.__class__).converter(
                value
            )
        if self.is_valid(value):
            self._value = value

    @classmethod
    @abstractmethod
    def is_valid(cls, value: T) -> bool:
        pass
