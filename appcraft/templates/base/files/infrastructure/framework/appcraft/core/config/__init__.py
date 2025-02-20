import os
from .toml import TomlConfig
from .json import JsonConfig
from .env import EnvConfig
from .base import BaseConfig


class Config(BaseConfig):  # Herda de BaseConfig
    def __init__(self, dir="config/"):
        extensions = ["json", "env", "toml"]
        super().__init__(extensions, dir)  # Chama o construtor da classe base

        # Inicializa as classes específicas para cada tipo de configuração
        self.toml_config = TomlConfig(dir)
        self.json_config = JsonConfig(dir)
        self.env_config = EnvConfig(dir)

    def _load_file(self, file_path):
        """Carrega um arquivo específico com base na sua extensão."""
        ext = os.path.splitext(file_path)[1]  # Obtém a extensão do arquivo
        if ext == ".json":
            return self.json_config._load_file(
                file_path
            )  # Ajuste conforme necessário
        elif ext == ".env":
            return self.env_config._load_file(
                file_path
            )  # Ajuste conforme necessário
        elif ext == ".toml":
            return self.toml_config._load_file(
                file_path
            )  # Ajuste conforme necessário
        else:
            raise ValueError("Unsupported file type")
