import json

from .base import BaseConfig


class JsonConfig(BaseConfig):
    EXTENSIONS = ["json"]

    def __init__(self, dir: str = "config"):
        super().__init__(dir)

    def load_file(self, file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)
