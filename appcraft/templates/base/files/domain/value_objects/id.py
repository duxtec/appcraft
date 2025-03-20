from domain.value_objects.base import ValueObjectBase
from domain.value_objects.converters.type_conversor import (
    ValueObjectTypeConversor,
)
from domain.value_objects.exceptions import (
    ValueObjectError,
    ValueObjectNonPositiveError,
)


class Id(ValueObjectBase[int]):
    def __init__(self, value: int | str) -> None:
        super().__init__(value)
        value = self.value
        if isinstance(value, str):
            value = ValueObjectTypeConversor(self.__class__).converter(value)

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
    def _is_positive(cls, value: int) -> bool:
        return value > 0
