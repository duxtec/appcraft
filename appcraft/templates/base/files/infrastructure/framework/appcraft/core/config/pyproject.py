from typing import Any, cast

import toml

from .base import BaseConfig


class PyProjectConfig(BaseConfig):
    EXTENSIONS = ["toml"]

    def __init__(self, dir: str = ""):
        super().__init__(dir)

    def _get_nested(self, data: dict[str, Any], dotted_key: str) -> Any:
        value: Any = data
        for part in dotted_key.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(part)
        return value

    def get(self, file_name: str) -> dict[str, Any]:
        # The app's own settings are not read from pyproject.toml at all —
        # config/app.toml is their single source of truth. Only other
        # templates' nested [tool.appcraft.<template>] tables go through
        # this lookup.
        if file_name == "app":
            return {}

        pyproject_file = self.load_file()
        pyproject_prop = pyproject_file.get(file_name)
        if isinstance(pyproject_prop, dict):
            configs: dict[str, Any] = cast(dict[str, Any], pyproject_prop)
        else:
            pyproject_prop = self._get_nested(
                pyproject_file, f"tool.appcraft.{file_name}"
            )
            if isinstance(pyproject_prop, dict):
                configs = cast(dict[str, Any], pyproject_prop)
            else:
                configs = {}

        return configs

    def load_file(self, file_path: str = "pyproject.toml") -> dict[str, Any]:
        try:
            with open(file_path, "r") as file:
                return toml.load(file)

        except Exception:
            return {}
