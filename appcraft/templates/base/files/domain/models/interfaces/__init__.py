from abc import ABC
from typing import Optional

from domain.value_objects.id import Id


class ModelInterface(ABC):
    _id: Optional[int] = None
    id: Optional[int]

    def __init__(self, id: Optional[int]) -> None:
        self.id = id

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        if value:
            self._id = Id(value).value
