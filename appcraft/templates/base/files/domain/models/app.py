from typing import Literal

from pydantic import field_validator

from domain.models import NewModel


class App(NewModel):
    name: str
    version: str
    environment: Literal['development', 'production']
    debug_mode: bool

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Name cannot be empty")

        return value

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: str) -> str:
        if not value:
            raise ValueError("Version cannot be empty")

        return value

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        if value not in ['development', 'production']:
            raise ValueError(
                "Environment must be 'development' or 'production'"
            )
        return value

    @field_validator("debug_mode")
    @classmethod
    def validate_debug_mode(cls, value: bool) -> bool:
        if not isinstance(value, bool):  # type: ignore[unnecessary-isinstance]
            raise TypeError("debug_mode must be a boolean")
        return value

    def __repr__(self):
        return (
            f"App(name={self.name}, version={self.version}, "
            f"environment={self.environment}, debug_mode={self.debug_mode})"
        )
