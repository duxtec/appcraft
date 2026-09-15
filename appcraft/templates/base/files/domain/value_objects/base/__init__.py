from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from domain.value_objects import ValueObject
from domain.value_objects.converters.type import ValueObjectTypeConversor
from domain.value_objects.exceptions import ValueObjectError

T = TypeVar("T")


class ValueObjectBase(ValueObject[T], Generic[T], ABC):
    def __init__(self, value: T | str) -> None:
        if isinstance(value, str):
            value = ValueObjectTypeConversor(self.__class__).converter(value)

        if not self.is_valid(value):
            raise ValueObjectError(value_object=self.__class__, value=value)

        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @classmethod
    @abstractmethod
    def is_valid(cls, value: T) -> bool:
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, "_value"):
            raise AttributeError("Value Objects are immutable.")
        object.__setattr__(self, name, value)

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ValueObjectBase):
            other_typed = cast(ValueObjectBase[Any], other)
            if type(self) is not type(other_typed):
                return False
            return bool(self._value == other_typed._value)
        return bool(self._value == other)

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value})"


class IntValueObject(ValueObjectBase[int]):
    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value


class StringValueObject(ValueObjectBase[str]):
    def __len__(self) -> int:
        return len(self._value)

    def __contains__(self, item: str) -> bool:
        return item in self._value
