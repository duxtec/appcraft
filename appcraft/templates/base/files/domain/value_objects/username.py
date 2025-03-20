from typing import Any

from domain.value_objects.base import ValueObjectBase
from domain.value_objects.exceptions import ValueObjectError


class Username(ValueObjectBase[str]):
    def __init__(self, value: Any) -> None:
        if not self.is_valid(value):
            raise self.Error.UsernameTooShort(value)
        self._value = value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        if len(value) < 5:
            return False
        return True

    class Error:
        class UsernameTooShort(ValueObjectError):
            def __init__(
                self,
                value: str,
                message: str = "Username must be at least 5 characters long.",
            ):
                super().__init__(
                    value_object=Username, value=value, message=message
                )
