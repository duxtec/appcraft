import toml

from .base import ConfigBase


class TomlConfig(ConfigBase):
    EXTENSIONS = ["toml"]

    def load_file(self, file_path: str):
        with open(file_path, "r") as file:
            return toml.load(file)
