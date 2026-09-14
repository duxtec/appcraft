from typing import Any

from .base import BaseConfig


class EnvConfig(BaseConfig):
    EXTENSIONS = ["env"]

    def load_file(self, file_path: str):
        config: dict[str, Any] = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
