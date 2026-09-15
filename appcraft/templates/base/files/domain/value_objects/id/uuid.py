from uuid import UUID

from domain.value_objects.base import ValueObjectBase


class UuidId(ValueObjectBase[UUID]):
    @classmethod
    def is_valid(cls, value: UUID) -> bool:
        return isinstance(
            value, UUID
        )  # pyright: ignore[reportUnnecessaryIsInstance]
