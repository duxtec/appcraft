import os
from datetime import datetime
from typing import List, Optional


class AppManager:
    _start_time = None

    @classmethod
    def get_start_time(self, format="%Y-%m-%d %H:%M:%S"):
        start_time = os.getenv("START_TIME")
        if start_time is None:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.environ["START_TIME"] = start_time

        start_time = datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        return start_time

    @classmethod
    def get_uptime(cls):
        start_time = cls.get_start_time()
        uptime = datetime.now() - datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S"
        )
        return str(uptime)

    @classmethod
    def name(self) -> bool:
        return self.environ_or_config(
            "APP_NAME", "name", "Appcraft"
        )

    @classmethod
    def version(self) -> bool:
        return self.environ_or_config(
            "APP_VERSION", "version", "0.0.1"
        )

    @classmethod
    def environment(self) -> str:
        return self.environ_or_config(
            "ENVIRONMENT", "environment", "development"
        )

    @classmethod
    def debug_mode(self) -> bool:
        return self.environ_or_config(
            "APP_DEBUG_MODE", "debug_mode"
        ).lower() == "true"

    @classmethod
    def log_level(self) -> str:
        return self.environ_or_config(
            "LOG_LEVEL", "log_level", "info"
        )

    @classmethod
    def lang(self) -> str:
        return self.environ_or_config(
            "LANG", "lang", "en"
        )

    @classmethod
    def lang_preference(self) -> str:
        return self.environ_or_config(
            "LANG_PREFERENCE", "lang_preference", "system"
        )

    @classmethod
    def supported_langs(self) -> List:
        return self.environ_or_config(
            "SUPPORTED_LANGS", "supported_langs", ["en"]
        ).split(",")

    @classmethod
    def config(self):
        try:
            from infrastructure.framework.appcraft.core.config\
                import Config

            return Config().get("app")
        except Exception:
            class Config:
                def get(*args, **kargs):
                    return None
        return None

    @classmethod
    def environ_or_config(
        cls, environ_name,
        config_name: Optional[str] = None, default_value=False
    ):
        if not config_name:
            config_name = environ_name

        value = str(
            os.getenv(environ_name)
            or (cls.config() and cls.config().get(config_name))
            or default_value
        )

        os.environ[environ_name] = value

        return value
