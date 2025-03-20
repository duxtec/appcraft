from abc import abstractmethod
from typing import Any


class DTOInterface:
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass
