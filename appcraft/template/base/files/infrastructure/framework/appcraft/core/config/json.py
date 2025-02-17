import json
from .base import BaseConfig


class JsonConfig(BaseConfig):
    def __init__(self, dir="config/"):
        super().__init__("json", dir)

    def _load_file(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)
