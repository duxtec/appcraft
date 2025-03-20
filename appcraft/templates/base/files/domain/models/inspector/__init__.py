from datetime import datetime
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from domain.models.exceptions import ModelPropertyValueError
from domain.models.interfaces import ModelInterface

ModelType = TypeVar("ModelType", bound=ModelInterface)
PropertyType = TypeVar("PropertyType", bound=property)


class ModelPropertyInspector(Generic[ModelType, PropertyType]):
    def __init__(self, model_property: PropertyType) -> None:
        self.prop = model_property
        self._cached_cls: Optional[ModelType] = None
        self._cached_type: Optional[Type[Any]] = None
        self._cached_name: Optional[str] = None

    @property
    def prop(self) -> PropertyType:
        return self._property

    @prop.setter
    def prop(self, value: PropertyType):
        if value.fget is None:
            raise ValueError("The property must have a getter method.")

        self._property = value

    @property
    def cls(self) -> ModelType:
        if not self._cached_cls:
            self._cached_cls = self._find_owner_class()
        return self._cached_cls

    @property
    def type(self) -> Type[PropertyType]:
        if not self._cached_type:
            self._cached_type = self._resolve_property_type()
        return self._cached_type

    @property
    def name(self) -> str:
        if not self._cached_name:
            self._cached_name = self._get_property_name()
        return self._cached_name

    def _find_owner_class(self) -> ModelType:
        if self.prop.fget is None:
            raise ValueError("The property must have a getter method.")

        model_name = self.prop.fget.__qualname__.split(".")[0]
        model = self.prop.fget.__globals__[model_name]
        return model

    def _resolve_property_type(self) -> Type[Any]:
        try:
            from typing import get_type_hints

            hints = get_type_hints(self.cls)
            return hints.get(self.name, self.cls)
        except Exception as e:
            raise TypeError(
                f"Could not resolve property type: {str(e)}"
            ) from e

    def _get_property_name(self) -> str:
        if self.prop.fset:
            return self.prop.fset.__name__
        raise AttributeError("Property has neither fget nor fset methods")

    def set(self, value: Any):
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
        converters: Dict[Type[Any], Callable[[str], Any]] = {
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
