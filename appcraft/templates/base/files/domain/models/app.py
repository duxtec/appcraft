from domain.app import Environment
from domain.models import NewModel
from domain.models.core.pydantic import field_validator


class App(NewModel):
    name: str
    version: str
    environment: Environment
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

    @field_validator("debug_mode")
    @classmethod
    def validate_debug_mode(cls, value: bool) -> bool:
        if not isinstance(value, bool):  # type: ignore[unnecessary-isinstance]
            raise TypeError("debug_mode must be a boolean")
        return value

    def __repr__(self):
        return (
            f"App(name={self.name}, version={self.version}, "
            f"environment={self.environment.value}, debug_mode={self.debug_mode})"
        )
