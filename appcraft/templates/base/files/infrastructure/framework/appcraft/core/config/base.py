import os
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    def __init__(self, extensions, dir="config"):
        self.dir = dir
        # Garante que seja uma lista
        self.extensions = (
            extensions if isinstance(extensions, list) else [extensions]
        )

    def _load(self):
        # Filtra os arquivos que têm as extensões especificadas
        files = [
            f
            for f in os.listdir(self.dir)
            if any(f.endswith(ext) for ext in self.extensions)
        ]
        configs = {}  # Variável local para armazenar configurações
        for file_name in files:
            file_path = os.path.join(self.dir, file_name)
            config = self._load_file(file_path)
            configs[os.path.splitext(file_name)[0]] = config
        return configs  # Retorna as configurações carregadas

    @abstractmethod
    def _load_file(self, file_path):  # pragma: no cover
        """Esse método deve ser implementado pelas subclasses
        para carregar arquivos específicos."""
        pass

    def get(self, file_name):
        # Filtra os arquivos que têm as extensões especificadas
        files = [
            f
            for f in os.listdir(self.dir)
            if any(f.endswith(f"{file_name}.{ext}") for ext in self.extensions)
        ]

        # Verifica se file_name está na lista de arquivos
        if not files:
            raise FileNotFoundError(
                f"\
The '{file_name}' setup file was not found in the '{self.dir}' folder."
            )

        file_path = os.path.join(self.dir, files[0])
        return self._load_file(file_path)
