from typing import Any, Optional

from domain.value_objects.interfaces import ValueObjectInterface


class ValueObjectError(Exception):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        self.value_object_name = value_object.__name__
        self.value = value

        if message:
            self.message = message
        else:
            self.message = f"\
Invalid value '{self.value}' for {self.value_object_name}."

        super().__init__(self.message)


class ValueObjectNonNumericError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{value_object.__name__} must be a numeric value."
        super().__init__(
            value_object=value_object, value=value, message=message
        )


class ValueObjectNonIntegerError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{value_object.__name__} must be a integer value."
        super().__init__(
            value_object=value_object, value=value, message=message
        )


class ValueObjectNonPositiveError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{value_object.__name__} must be a positive integer."
        super().__init__(
            value_object=value_object, value=value, message=message
        )


class ValueObjectNonBooleanError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"{value_object.__name__} must be 'true' or 'false'"
        super().__init__(
            value_object=value_object, value=value, message=message
        )


class ValueObjectNonDatetimeError(ValueObjectError):
    def __init__(
        self,
        value_object: type[ValueObjectInterface],
        value: Any,
        message: Optional[str] = None,
    ):
        if not message:
            message = f"\
{value_object.__name__} \
must be a valid datetime format (expected YYYY-MM-DD[ HH:MM:SS])."
        super().__init__(
            value_object=value_object, value=value, message=message
        )
