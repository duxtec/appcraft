import os
from datetime import datetime
from typing import Any, Literal


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
                def get(self, file_name: str) -> dict[str, Any]:
                    return {}

            self._config = Config()

    @property
    def start_time(self) -> str:
        start_time = os.getenv("START_TIME")
        if start_time is None:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.environ["START_TIME"] = start_time

        return start_time

    def format_start_time(self, format: str) -> str:
        return datetime.strptime(
            self.start_time, "%Y-%m-%d %H:%M:%S"
        ).strftime(format)

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
    def description(self) -> str:
        return self.environ_or_config("description", "Appcraft")

    @property
    def version(self) -> str:
        return self.environ_or_config("version", "0.0.1")

    @property
    def environment(self) -> Literal["production", "development"]:
        return self.environ_or_config("environment", "development")

    @property
    def debug_mode(self) -> bool:
        return self.environ_or_config("debug_mode", False)

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
    def supported_langs(self) -> list[str]:
        return self.environ_or_config("supported_langs", ["en"]).split(",")

    @property
    def theme(self) -> Literal["dark", "light"]:
        return self.environ_or_config("theme", "dark")

    @property
    def config(self) -> dict[str, Any]:
        return self._config.get("app")

    def environ_or_config(
        self,
        config_name: str,
        default_value: Any = False,
    ) -> Any:
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

        if isinstance(default_value, bool) and isinstance(value, str):
            value = value.strip().lower() in ("true", "1", "yes", "y", "on")

        if isinstance(value, str):
            os.environ[f"APPCRAFT_{environ_name}"] = value

        return value
