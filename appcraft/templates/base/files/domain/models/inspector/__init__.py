from datetime import datetime
from typing import Any, Callable, Dict, Optional, Type

from domain.models.exceptions import ModelPropertyValueError
from domain.models.interfaces import ModelInterface


class ModelPropertyInspector:
    def __init__(self, model_property: property) -> None:
        self._cached_cls = None
        self._property = model_property
        self._cached_type: Optional[Type] = None
        self._cached_name: Optional[str] = None

        if not isinstance(model_property, property) and not isinstance(
            model_property, property
        ):
            raise TypeError("Must provide a valid property")

        if not issubclass(self.cls, ModelInterface):
            raise TypeError(
                f"\
The {self.cls} class of {model_property} \
property must inherit from ModelInterface."
            )

    @property
    def prop(self) -> property:
        return self._property

    @property
    def cls(self) -> ModelInterface:
        if not self._cached_cls:
            self._cached_cls = self._find_owner_class()
        return self._cached_cls

    @property
    def type(self) -> Type:
        if not self._cached_type:
            self._cached_type = self._resolve_property_type()
        return self._cached_type

    @property
    def name(self) -> str:
        if not self._cached_name:
            self._cached_name = self._get_property_name()
        return self._cached_name

    def _find_owner_class(self) -> ModelInterface:
        model_name = self.prop.fget.__qualname__.split(".")[0]
        model = self.prop.fget.__globals__[model_name]
        return model

    def _resolve_property_type(self) -> Type:
        try:
            from typing import get_type_hints

            hints = get_type_hints(self.cls)
            return hints.get(self.name, object)
        except Exception as e:
            raise TypeError(
                f"Could not resolve property type: {str(e)}"
            ) from e

    def _get_property_name(self) -> str:
        if self.prop.fget:
            return self.prop.fget.__name__
        if self.prop.fset:
            return self.prop.fset.__name__
        raise AttributeError("Property has neither fget nor fset methods")

    def set(self, value):
        self.prop.__set__(self.cls, value)

    def __repr__(self) -> str:
        return (
            f"<ModelProperty {self.name} of {self.cls.__name__} ({self.type})>"
        )


class ModelPropertyTypeConversor:
    def __init__(self, model_property: property) -> None:
        self.model_property: ModelPropertyInspector = ModelPropertyInspector(
            model_property
        )

    def converter(self, value: str) -> Any:
        type = self.model_property.type
        converters: Dict[Type, Callable[[str], Any]] = {
            int: self._convert_int,
            float: self._convert_float,
            bool: self._convert_bool,
            datetime: self._convert_datetime,
            str: lambda x: x.strip(),
        }
        return converters.get(type, lambda x: x)(value)

    def _convert_int(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ModelPropertyValueError(
                model_property=self.model_property.property,
                value=value,
                message=f"{self.model_property.name} must be a valid integer",
            )

    def _convert_float(self, value: str) -> float:
        try:

            return float(value)
        except ValueError:
            raise ModelPropertyValueError(
                model_property=self.model_property.property,
                value=value,
                message=f"\
{self.model_property.name} must be a valid decimal number",
            )

    def _convert_bool(self, value: str) -> bool:
        lower = value.lower()
        if lower in ("true", "t", "1", "yes", "y"):
            return True
        if lower in ("false", "f", "0", "no", "n"):
            return False
        raise ModelPropertyValueError(
            model_property=self.model_property.property,
            value=value,
            message=f"\
{self.model_property.name} must be 'true' or 'false'",
        )

    def _convert_datetime(self, value: str) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ModelPropertyValueError(
                model_property=self.model_property.prop,
                value=value,
                message=f"\
{self.model_property.name}: \
Invalid datetime format (expected YYYY-MM-DD[ HH:MM:SS]).",
            )
