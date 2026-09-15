from typing import Any

from domain.models import NewModel


class ModelNotFoundError(Exception):
    def __init__(self, model: type[NewModel]) -> None:
        self.message = f"The {model.__name__} has not found"
        super().__init__(self.message)


class ModelPropertyValueError(Exception):
    def __init__(
        self,
        model_property: property,
        value: Any,
        message: str | None = None,
    ):
        fget = model_property.fget

        if fget is None:
            raise AttributeError("Property has no getter")

        self.model_name = fget.__qualname__.split(".")[0]
        self.model_property = fget.__name__
        self.model = fget.__globals__[self.model_name]
        self.value = value

        if message:
            self.message = message
        else:
            self.message = f"\
{self.model_property} from {self.model_name}: Value model property error"

        super().__init__(self.message)
