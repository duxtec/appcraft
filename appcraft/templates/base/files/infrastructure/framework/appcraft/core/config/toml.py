import toml

from .base import BaseConfig


class TomlConfig(BaseConfig):
    EXTENSIONS = ["toml"]

    def load_file(self, file_path: str):
        with open(file_path, "r") as file:
            return toml.load(file)
