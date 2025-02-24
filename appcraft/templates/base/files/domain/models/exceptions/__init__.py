from typing import Any, Optional

from domain.models.interfaces import ModelInterface


class ModelNotFoundError(Exception):
    def __init__(self, model: type[ModelInterface]) -> None:
        self.message = f"The {model.__name__} has not found"
        super().__init__(self.message)


class ModelPropertyValueError(Exception):
    def __init__(
        self,
        model_property: property,
        value: Any,
        message: Optional[str] = None,
    ):
        self.model_name = model_property.fget.__qualname__.split(".")[0]
        self.model_property = model_property.fget.__name__
        self.model = model_property.fget.__globals__[self.model_name]
        self.value = value

        if message:
            self.message = message
        else:
            self.message = f"\
{self.model_property} from {self.model_name}: Value model property error"

        super().__init__(self.message)
