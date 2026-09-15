from __future__ import annotations

from typing import Any, Iterator, Self, cast, overload

from domain.models.core.field import Field
from domain.models.core.pydantic import IdType
from domain.value_objects.id import Id


class Keys:
    """Represents a collection of identifier fields."""

    def __init__(self) -> None:
        self._keys: dict[Field[Any], Any] = {}

    def set(
        self,
        field: Field[IdType],
        value: IdType,
    ) -> Self:
        """
        Adds or replaces an identifier.

        Raises:
            TypeError: If the value is incompatible with the field.
        """
        # If Field implements validation:
        # field.validate(value)

        self._keys[field] = value
        return self

    @overload
    def get(self, field: Field[IdType]) -> IdType | None: ...

    @overload
    def get(
        self,
        field: Field[IdType],
        default: IdType,
    ) -> IdType: ...

    def get(
        self,
        field: Field[IdType],
        default: IdType | None = None,
    ) -> IdType | None:
        return self._keys.get(field, default)

    def remove(self, field: Field[Any]) -> Self:
        self._keys.pop(field, None)
        return self

    def clear(self) -> Self:
        self._keys.clear()
        return self

    def contains(self, field: Field[Any]) -> bool:
        return field in self._keys

    def items(self) -> Iterator[tuple[Field[Any], Any]]:
        return iter(self._keys.items())

    def fields(self) -> Iterator[Field[Any]]:
        return iter(self._keys.keys())

    def values(self) -> Iterator[Any]:
        return iter(self._keys.values())

    def as_dict(self) -> dict[Field[Any], Any]:
        return self._keys.copy()

    def __getitem__(self, field: Field[IdType]) -> IdType:
        value = self._keys[field]

        if not isinstance(value, Id):
            raise TypeError(
                f"Expected an Id for field '{field}', "
                f"got {type(value).__name__}."
            )

        return cast(IdType, value)

    def __contains__(self, field: object) -> bool:
        return field in self._keys

    def __iter__(self) -> Iterator[tuple[Field[Any], Any]]:
        return iter(self._keys.items())

    def __len__(self) -> int:
        return len(self._keys)

    def __bool__(self) -> bool:
        return bool(self._keys)

    def __repr__(self) -> str:
        content = ", ".join(
            f"{field}={value!r}" for field, value in self._keys.items()
        )
        return f"{self.__class__.__name__}({content})"
