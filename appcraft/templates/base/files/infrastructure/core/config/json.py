import json

from .base import ConfigBase


class JsonConfig(ConfigBase):
    EXTENSIONS = ["json"]

    def load_file(self, file_path: str):
        with open(file_path, "r") as file:
            return json.load(file)
