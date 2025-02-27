import os
from typing import Any, Dict

from .base import BaseConfig
from .env import EnvConfig
from .json import JsonConfig
from .pyproject import PyProjectConfig
from .toml import TomlConfig


class Config(BaseConfig):
    EXTENSIONS = ["json", "env", "toml"]

    def __init__(self, dir="config"):
        super().__init__(dir)

        self.pyproject_config = PyProjectConfig()
        self.toml_config = TomlConfig(dir)
        self.json_config = JsonConfig(dir)
        self.env_config = EnvConfig(dir)

    def get(self, file_name: str) -> Dict[str, Any]:
        try:
            configs = self.pyproject_config.get(file_name)

            if configs:
                self.loaded_files[file_name] = configs
                return configs
        except Exception:
            pass

        return super().get(file_name)

    def _load_file(self, file_path) -> Dict[str, Any]:
        try:
            pyproject_config = self.pyproject_config.get(file_path)
            if pyproject_config:
                return self.pyproject_config._load_file(file_path)
        except Exception:
            pass

        ext = os.path.splitext(file_path)[1]

        if ext == ".json":
            return self.json_config._load_file(file_path)
        elif ext == ".env":
            return self.env_config._load_file(file_path)
        elif ext == ".toml":
            return self.toml_config._load_file(file_path)
        else:
            raise ValueError("Unsupported file type")
