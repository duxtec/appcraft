import os
from datetime import datetime
from typing import Any, Dict, List


class AppManager:
    _start_time = None

    def __init__(self):
        try:
            from infrastructure.framework.appcraft.core.config import (
                Config as ExternalConfig,
            )

            self._config = ExternalConfig()
        except Exception:

            class Config:
                def get(self, file_name: str) -> Dict[str, Any]:
                    return {}

            self._config = Config()

    @property
    def start_time(self, format="%Y-%m-%d %H:%M:%S") -> str:
        start_time = os.getenv("START_TIME")
        if start_time is None:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.environ["START_TIME"] = start_time

        if format != "%Y-%m-%d %H:%M:%S":
            start_time = datetime.strptime(
                start_time, "%Y-%m-%d %H:%M:%S"
            ).strftime(format)

        return start_time

    @property
    def uptime(self):
        start_time = self.start_time
        uptime = datetime.now() - datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S"
        )
        return str(uptime)

    @property
    def name(self) -> str:
        return self.environ_or_config("name", "Appcraft")

    @property
    def version(self) -> str:
        return self.environ_or_config("version", "0.0.1")

    @property
    def environment(self) -> str:
        return self.environ_or_config("environment", "development")

    @property
    def debug_mode(self) -> bool:
        return self.environ_or_config("debug_mode")

    @property
    def log_level(self) -> str:
        return self.environ_or_config("log_level", "info")

    @property
    def lang(self) -> str:
        return self.environ_or_config("lang", "en")

    @property
    def lang_preference(self) -> str:
        return self.environ_or_config("lang_preference", "system")

    @property
    def supported_langs(self) -> List:
        return self.environ_or_config("supported_langs", ["en"]).split(",")

    @property
    def config(self) -> Dict[str, Any]:
        return self._config.get("app")

    def environ_or_config(
        self,
        config_name: str,
        default_value: Any = False,
    ):
        environ_name = config_name.upper()
        if not config_name:
            config_name = environ_name

        value = (
            os.getenv(f"APPCRAFT_{environ_name}")
            or os.getenv(f"APP_{environ_name}")
            or os.getenv(environ_name)
            or self.config.get(config_name)
            or default_value
        )

        if isinstance(value, str):
            os.environ[f"APPCRAFT_{environ_name}"] = value

        return value
