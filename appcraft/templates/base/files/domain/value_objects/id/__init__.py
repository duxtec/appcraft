from domain.value_objects.base import IntValueObject

# domain/value_objects/ids/exceptions.py
from domain.value_objects.exceptions import ValueObjectError


class IdNotPositiveError(ValueObjectError):
    def __str__(self) -> str:
        return f"{self.value_object_name} must be positive, got {self.value}"


class Id(IntValueObject):
    @classmethod
    def is_valid(cls, value: int) -> bool:
        if value <= 0:
            raise IdNotPositiveError(value_object=cls, value=value)
        return True
