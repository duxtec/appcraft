from abc import ABC
from typing import Optional

from domain.value_objects.id import Id


class ModelInterface(ABC):
    def __init__(self, id: Optional[int]) -> None:
        if id is None:
            self._id = id
        else:
            self.id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        self._id = Id(value).value
