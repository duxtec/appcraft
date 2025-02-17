from domain.models.app import App
from infrastructure.framework.appcraft.core.config import Config


class AppService:
    def __init__(self, config=None):
        self.info = config if config is not None else Config().get("app")

    def get_app(self):
        app = App(
            name=self.info["name"],
            version=self.info["version"],
            environment=self.info["environment"],
            debug_mode=self.info["debug_mode"],
            log_level=self.info["log_level"],
            language=self.info["lang"],
            language_preference=self.info["lang_preference"],
            supported_languages=self.info["supported_langs"]
        )
        return app
