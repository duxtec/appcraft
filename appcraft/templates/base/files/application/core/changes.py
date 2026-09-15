from __future__ import annotations

from typing import Any, Iterator, Self, TypeVar

from domain.models.core.field import Field

ValueType = TypeVar("ValueType")


class Changes:
    """Represents a collection of validated field changes."""

    def __init__(self) -> None:
        self._changes: dict[Field[Any], Any] = {}

    def set(
        self,
        field: Field[ValueType],
        value: ValueType,
    ) -> Self:
        """
        Adds or replaces a field change.

        Raises:
            TypeError: If the value is not compatible with the field.
        """
        self._changes[field] = value
        return self

    def remove(self, field: Field[Any]) -> Self:
        """Removes a field from the change set."""
        self._changes.pop(field, None)
        return self

    def clear(self) -> Self:
        """Removes all changes."""
        self._changes.clear()
        return self

    def get(
        self,
        field: Field[ValueType],
        default: ValueType | None = None,
    ) -> ValueType | None:
        """Returns the value associated with a field."""
        return self._changes.get(field, default)

    def contains(self, field: Field[Any]) -> bool:
        """Checks whether a field has a pending change."""
        return field in self._changes

    def items(self) -> Iterator[tuple[Field[Any], Any]]:
        """Iterates over all field/value pairs."""
        return iter(self._changes.items())

    def fields(self) -> Iterator[Field[Any]]:
        """Iterates over changed fields."""
        return iter(self._changes.keys())

    def values(self) -> Iterator[Any]:
        """Iterates over changed values."""
        return iter(self._changes.values())

    def as_dict(self) -> dict[Field[Any], Any]:
        """Returns a shallow copy of the internal mapping."""
        return self._changes.copy()

    def __getitem__(self, field: Field[ValueType]) -> ValueType:
        return self._changes[field]

    def __contains__(self, field: object) -> bool:
        return field in self._changes

    def __iter__(self) -> Iterator[tuple[Field[Any], Any]]:
        return self.items()

    def __len__(self) -> int:
        return len(self._changes)

    def __bool__(self) -> bool:
        return bool(self._changes)
