import toml
from .base import BaseConfig


class TomlConfig(BaseConfig):
    def __init__(self, dir="config/"):
        super().__init__("toml", dir)

    def _load_file(self, file_path):
        with open(file_path, "r") as file:
            return toml.load(file)  # Carrega a partir do objeto de arquivo
