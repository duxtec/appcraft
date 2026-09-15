from domain.value_objects.base import StringValueObject


class UlidId(StringValueObject):
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return len(value) == 26 and value.isalnum()
