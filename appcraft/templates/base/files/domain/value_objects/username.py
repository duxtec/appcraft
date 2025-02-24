from typing import Any

from domain.value_objects.exceptions import ValueObjectError
from domain.value_objects.interfaces import ValueObjectInterface


class Username(ValueObjectInterface[str]):
    def __init__(self, value: Any) -> None:
        if not self.is_valid(value):
            raise self.Error.UsernameTooShort(value)
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def is_valid(cls, username: str) -> bool:
        if len(username) < 5:
            return False
        return True

    class Error:
        class UsernameTooShort(ValueObjectError):
            def __init__(
                self,
                value,
                message="Username must be at least 5 characters long.",
            ):
                super().__init__(
                    value_object=Username, value=value, message=message
                )
