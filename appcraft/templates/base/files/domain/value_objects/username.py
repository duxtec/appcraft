from typing import Any

from domain.value_objects.base import ValueObjectBase
from domain.value_objects.exceptions import ValueObjectError


class UsernameTooShortError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectBase[Any]],
        value: Any,
        message: str | None = None,
    ) -> None:
        if not message:
            message = "Username must be at least 5 characters long."
        super().__init__(
            value_object=value_object, value=value, message=message
        )


class Username(ValueObjectBase[str]):
    @classmethod
    def is_valid(cls, value: str) -> bool:
        if len(value) < 5:
            raise UsernameTooShortError(value_object=cls, value=value)
        return True
