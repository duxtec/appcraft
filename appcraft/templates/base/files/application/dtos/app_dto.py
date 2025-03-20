from typing import Any

from application.dtos.interfaces import DTOInterface


class AppDTO(DTOInterface):
    def __init__(
        self, name: str, version: str, environment: str, debug_mode: bool
    ):
        self.name = name
        self.version = version
        self.environment = environment
        self.debug_mode = debug_mode

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "debug_mode": self.debug_mode,
        }
