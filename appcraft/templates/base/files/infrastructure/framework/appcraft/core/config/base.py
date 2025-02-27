import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseConfig(ABC):
    EXTENSIONS: List[str]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'EXTENSIONS') or cls.EXTENSIONS is None:
            raise TypeError(f"{cls.__name__} must define 'EXTENSIONS'.")
        return super().__new__(cls)

    def __init__(self, dir: str = "config"):
        self.dir = dir
        self.loaded_files: Dict[str, Any] = {}

    def _load(self) -> Dict[str, Any]:
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
    def _load_file(self, file_path: str) -> Dict[str, Any]:
        pass

    def get(self, file_name: str) -> Dict[str, Any]:
        if file_name in self.loaded_files:
            return self.loaded_files[file_name]

        files = [
            f
            for f in os.listdir(self.dir)
            if any(f.endswith(f"{file_name}.{ext}") for ext in self.EXTENSIONS)
        ]

        try:
            file_path = os.path.join(self.dir, files[0])
            loaded_file = self._load_file(file_path)
            self.loaded_files[file_name] = loaded_file
            return loaded_file
        except Exception:
            return {}
