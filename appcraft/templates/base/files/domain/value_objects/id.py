from domain.value_objects.converters.type_conversor import (
    ValueObjectTypeConversor,
)
from domain.value_objects.exceptions import (
    ValueObjectError,
    ValueObjectNonIntegerError,
    ValueObjectNonPositiveError,
)
from domain.value_objects.interfaces import ValueObjectInterface


class Id(ValueObjectInterface[int]):
    def __init__(self, value: int) -> None:
        value = ValueObjectTypeConversor(self.__class__).converter(value)

        if not self._is_int(value):
            raise ValueObjectNonIntegerError(
                value_object=self.__class__, value=value
            )

        if not self._is_positive(value):
            raise ValueObjectNonPositiveError(
                value_object=self.__class__, value=value
            )

        if not self.is_valid(value):
            raise ValueObjectError(value_object=self.__class__, value=value)

        self._value = value

    @classmethod
    def is_valid(cls, value: int) -> bool:
        return cls._is_positive(value)

    @classmethod
    def _is_int(cls, value: int) -> bool:
        return isinstance(value, int)

    @classmethod
    def _is_positive(cls, value: int) -> bool:
        return cls._is_int(value) and value > 0
