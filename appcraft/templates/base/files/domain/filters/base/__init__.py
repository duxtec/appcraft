from abc import ABC
from typing import (
    Generic,
    Optional,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from domain.filters.interface import FilterInterface
from domain.models.interfaces import ModelInterface

Value = TypeVar("Value")


class FilterBase(FilterInterface, Generic[Value], ABC):
    value: Value

    def __init__(
        self,
        model_property: property,
        value: Value,
        include: Optional[bool] = None,
        not_param: Optional[bool] = None,
    ):
        if not isinstance(model_property, property):
            raise TypeError(
                f"The model_property {model_property} must be a property."
            )

        if model_property.fget is None:
            raise ValueError("The model_property must have a getter method.")

        model_name = model_property.fget.__qualname__.split(".")[0]
        model = model_property.fget.__globals__[model_name]

        value_type = type[value]
        expected_type = self.__annotations__['value']
        expected_origin = get_origin(expected_type) or expected_type
        expected_types = (
            get_args(expected_type)
            if get_args(expected_type)
            else (expected_origin,)
        )

        model_property_type = get_type_hints(model_property.fget).get(
            "return", None
        )

        model_property_origin = (
            get_origin(model_property_type) or model_property_type
        )

        model_property_types = (
            get_args(model_property_type)
            if get_args(model_property_type)
            else (model_property_origin,)
        )

        try:
            any(issubclass(value_type, t) for t in model_property_types)
        except TypeError:
            raise TypeError(
                f"\
Types mismatch: value_type={value_type}, \
expected_type={expected_type}, \
model_property_type={model_property_type}"
            )

        if not issubclass(model, ModelInterface):
            raise TypeError(
                f"\
The class of {model_property} must inherit from ModelInterface."
            )

        self.model = model
        self.property = model_property.fget.__name__
        self.value = value
        self.not_param = not_param
        self.include = include

    def _verify_types(self):
        pass

    def __repr__(self):
        props_repr = []
        props_repr.append(f"model={self.model}")
        props_repr.append(f"property={self.property}")
        props_repr.append(f"value={self.value}")

        if self.not_param is not None:
            props_repr.append(f"not_param={self.not_param}")

        if self.include is not None:
            props_repr.append(f"include={self.include}")

        props_repr_str = ", ".join(props_repr)

        return f"<{self.__class__.__name__}({props_repr_str})>"
