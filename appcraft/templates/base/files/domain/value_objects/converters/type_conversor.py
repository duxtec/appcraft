from datetime import datetime
from typing import Any, Callable, Dict, Type, TypeVar, get_args, get_type_hints

from domain.value_objects.exceptions import (
    ValueObjectNonBooleanError,
    ValueObjectNonDatetimeError,
    ValueObjectNonIntegerError,
    ValueObjectNonNumericError,
)
from domain.value_objects.interfaces import ValueObjectInterface


class ValueObjectTypeConversor:
    def __init__(self, value_object: type[ValueObjectInterface]) -> None:
        self.value_object: type[ValueObjectInterface] = value_object

    def converter(self, value: str) -> Any:
        type = get_type_hints(self.value_object).get("value")

        if isinstance(type, TypeVar):
            type = get_args(self.value_object.__orig_bases__[0])[0]

        converters: Dict[Type, Callable[[str], Any]] = {
            int: self._convert_int,
            float: self._convert_float,
            bool: self._convert_bool,
            datetime: self._convert_datetime,
            str: lambda x: str(x.strip()),
        }
        return converters.get(type, lambda x: x)(value)

    def _convert_int(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueObjectNonIntegerError(
                value_object=self.value_object, value=value
            )

    def _convert_float(self, value: str) -> float:
        try:
            return float(value)
        except ValueError:
            raise ValueObjectNonNumericError(
                value_object=self.value_object, value=value
            )

    def _convert_bool(self, value: str) -> bool:
        lower = value.lower()
        if lower in ("true", "t", "1", "yes", "y"):
            return True
        if lower in ("false", "f", "0", "no", "n"):
            return False
        raise ValueObjectNonBooleanError(
            value_object=self.value_object, value=value
        )

    def _convert_datetime(self, value: str) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError:

            raise ValueObjectNonDatetimeError(
                value_object=self.value_object, value=value
            )
