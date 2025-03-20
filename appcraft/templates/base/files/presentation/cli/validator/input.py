from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    cast,
    get_type_hints,
)

from domain.value_objects.interfaces import ValueObjectInterface
from infrastructure.framework.appcraft.core.property_meta import (
    PropertySetter,
)
from infrastructure.framework.appcraft.utils.printer import Printer

BasicType = TypeVar("BasicType", bound=Any)
PropertyType = TypeVar("PropertyType", bound=property)
ValueObjectType = TypeVar("ValueObjectType", bound=ValueObjectInterface[Any])


class CLIValidator(
    PropertySetter,
    Generic[BasicType],
    ABC,
):
    reference: type[BasicType]
    _props = ["reference"]

    @classmethod
    def input(
        cls,
        prompt: str,
        value: (
            str | int | dict[Any, Any] | list[Any] | BasicType | None
        ) = None,
        error_action: Optional[
            Callable[[Exception, Optional[str]], None]
        ] = None,
        error_message: Optional[str] = None,
        max_attempts: Optional[int] = 3,
    ) -> BasicType:
        attempts = 0

        while max_attempts is None or attempts < max_attempts:
            if value is None:
                value = input(prompt)
                print()
            try:
                return cls._validate(value)
            except Exception as e:
                value = None
                attempts += 1
                if error_action:
                    error_action(e, str(value))
                elif error_message:
                    Printer.warning(error_message)
                    print()
                else:
                    Printer.warning(str(e))
                    print()
                if max_attempts is not None and attempts >= max_attempts:
                    raise e

        raise ValueError(
            f"\
Exceeded maximum attempts ({max_attempts}). Input validation failed."
        )

    @classmethod
    @abstractmethod
    def _validate(cls, value: Any) -> BasicType: ...


class InputCLI(CLIValidator[BasicType], Generic[BasicType]):
    @classmethod
    def _validate(cls, value: BasicType) -> BasicType:
        if isinstance(cls.reference, ValueObjectInterface):
            return ValueObjectInput[BasicType]._validate(value)  # type: ignore
        if isinstance(cls.reference, property):
            return PropertyInput[BasicType]._validate(value)  # type: ignore
        else:
            return BasicTypeInput[BasicType]._validate(value)  # type: ignore


class ValueObjectInput(
    CLIValidator[ValueObjectType], Generic[ValueObjectType]
):
    reference: type[ValueObjectType]

    @classmethod
    def _validate(cls, value: ValueObjectType) -> ValueObjectType:
        value_object = cls.reference(value)
        return value_object


class PropertyInput(CLIValidator[PropertyType], Generic[PropertyType]):
    reference: type[PropertyType]

    @classmethod
    def _validate(cls, value: PropertyType) -> PropertyType:
        if cls.reference.fget is None:
            raise ValueError("The property must have a getter method.")

        model_name = cls.reference.fget.__qualname__.split(".")[0]
        model = cls.reference.fget.__globals__.get(model_name)

        if model is None or not isinstance(model, type):
            raise ValueError(
                f"\
Could not determine the model for property {cls.reference.fget.__name__}"
            )

        type_hints = get_type_hints(model)
        expected_type: type[Any] = type_hints.get(
            cls.reference.fget.__name__, Any
        )

        try:
            converted_value = expected_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"\
Invalid value for {cls.reference.fget.__name__}: \
expected {expected_type}, got {type(value).__name__}"
            ) from e

        if isinstance(cls.reference, property):
            cls.reference.__set__(model, converted_value)
        return cast(PropertyType, cls.reference)


class BasicTypeInput(CLIValidator[BasicType], Generic[BasicType]):

    @classmethod
    def _validate(cls, value: str | BasicType) -> BasicType:
        return cls._convert_value(value)

    @classmethod
    def _convert_value(cls, value: Any) -> BasicType:
        if cls.reference is bool:
            lower_value = str(value).strip().lower()
            if lower_value in ("true", "t", "1", "yes", "y"):
                return True  # type: ignore
            if lower_value in ("false", "f", "0", "no", "n"):
                return False  # type: ignore
            raise ValueError(
                f"\
Invalid boolean value: {value}. Expected 'true/false', 'y/n', '1/0'."
            )

        return cls.reference(value)
