from abc import ABC, abstractmethod
from typing import Any, Optional


class FilterInterface(ABC):
    @abstractmethod
    def __init__(
        self,
        model_property: property,
        value: Any,
        include: Optional[bool] = None,
        not_param: Optional[bool] = None,
    ):
        pass
