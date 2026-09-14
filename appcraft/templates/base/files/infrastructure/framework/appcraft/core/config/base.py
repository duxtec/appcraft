import os
from abc import ABC, abstractmethod
from typing import Any


class BaseConfig(ABC):
    EXTENSIONS: list[str]

    def __new__(cls, *args: Any, **kwargs: Any):
        if not hasattr(cls, 'EXTENSIONS') or not cls.EXTENSIONS:
            raise TypeError(f"{cls.__name__} must define 'EXTENSIONS'.")
        return super().__new__(cls)

    def __init__(self, dir: str = "config"):
        self.dir = dir
        self.loaded_files: dict[str, Any] = {}

    def _load(self) -> dict[str, Any]:
        files = [
            f
            for f in os.listdir(self.dir)
            if any(f.endswith(ext) for ext in self.EXTENSIONS)
        ]
        for file_name in files:
            file_path = os.path.join(self.dir, file_name)
            self.get(file_path)
        return self.loaded_files

    @abstractmethod
    def load_file(self, file_path: str) -> dict[str, Any]:
        pass

    def get(self, file_name: str) -> dict[str, Any]:
        if file_name in self.loaded_files:
            return self.loaded_files[file_name]

        files = [
            f
            for f in os.listdir(self.dir)
            if any(
                f.endswith(f"{file_name}.{ext}") for ext in self.EXTENSIONS
            )
        ]

        try:
            file_path = os.path.join(self.dir, files[0])
            loaded_file = self.load_file(file_path)
            self.loaded_files[file_name] = loaded_file
            return loaded_file
        except Exception:
            return {}
