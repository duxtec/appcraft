from typing import TypeVar

from domain.models.interfaces import ModelInterface

ModelType = TypeVar("ModelType", bound=ModelInterface)
