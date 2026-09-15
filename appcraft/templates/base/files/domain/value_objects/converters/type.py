from datetime import datetime
from typing import (
    Any,
    Callable,
    Generic,
    Type,
    TypeVar,
    get_args,
    get_type_hints,
)
from uuid import UUID

from domain.value_objects import ValueObject
from domain.value_objects.exceptions import (
    ValueObjectNonBooleanError,
    ValueObjectNonDatetimeError,
    ValueObjectNonIntegerError,
    ValueObjectNonNumericError,
    ValueObjectNonUuidError,
)

T = TypeVar("T")


class ValueObjectTypeConversor(Generic[T]):
    def __init__(self, value_object: type[ValueObject[T]]) -> None:
        self.value_object = value_object

    def converter(self, value: str) -> T:
        type_ = get_type_hints(self.value_object).get("_value")

        if isinstance(type_, TypeVar):
            origin_base: list[Any] = getattr(
                self.value_object, "__orig_bases__"
            )[0]
            type_ = get_args(origin_base)[0]

        converters: dict[Type[Any] | None, Callable[[str], Any]] = {
            int: self._convert_int,
            float: self._convert_float,
            bool: self._convert_bool,
            datetime: self._convert_datetime,
            UUID: self._convert_uuid,
            str: lambda x: str(x.strip()),
        }
        return converters.get(type_, lambda x: x)(value)

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

    def _convert_uuid(self, value: str) -> UUID:
        try:
            return UUID(value)
        except ValueError:
            raise ValueObjectNonUuidError(
                value_object=self.value_object, value=value
            )
