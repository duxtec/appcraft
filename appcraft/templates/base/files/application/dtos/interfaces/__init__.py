from abc import abstractmethod
from typing import Any, Dict


class DTOInterface:
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
