from typing import Any, Dict

import toml

from .base import BaseConfig


class PyProjectConfig(BaseConfig):
    EXTENSIONS = ["toml"]

    def __init__(self, dir: str = ""):
        super().__init__(dir)

    def get(self, file_name: str) -> Dict[str, Any]:
        pyproject_file = self._load_file()
        pyproject_prop = pyproject_file.get(file_name)
        if isinstance(pyproject_prop, dict):
            configs: Dict[str, Any] = pyproject_prop
        else:
            pyproject_prop = pyproject_file.get(f"tool.appcraft.{file_name}")
            if isinstance(pyproject_prop, dict):
                configs: Dict[str, Any] = pyproject_prop
            else:
                configs = {}

        if file_name == "app":
            app_infos: Dict[str, Any] = pyproject_file.get("tool.poetry") or {}
            configs.update(app_infos)

        return configs

    def _load_file(self, file_path: str = "pyproject.toml") -> Dict[str, Any]:
        try:
            with open(file_path, "r") as file:
                return toml.load(file)

        except Exception:
            return {}
