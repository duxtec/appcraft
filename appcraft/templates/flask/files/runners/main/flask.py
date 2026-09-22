import os
from typing import Any

from infrastructure.framework.appcraft.core.config import Config
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.framework.flask.app import FlaskApp

_DEFAULT_PORT = 5000


class Flask(Runner):
    @Runner.runner
    def start(self):
        app_config = Config().get("app")
        port = int(os.environ.get("PORT", _DEFAULT_PORT))

        if app_config.get("environment") == "production":
            self._start_production(port)
        else:
            FlaskApp().app.run(
                host="0.0.0.0",
                port=port,
                debug=bool(app_config.get("debug_mode", True)),
            )
        return False

    def _start_production(self, port: int) -> None:
        # Local import: gunicorn doesn't support Windows (no fcntl), and
        # every runners/main file gets imported just to discover its
        # Runner subclasses (RunnerDiscovery.get_apps) — a module-level
        # import here would break that discovery for anyone developing
        # on Windows, even if they never run this in production. Only
        # resolves for pyright when gunicorn (this template's own
        # pyproject.toml fragment) is installed.
        from gunicorn.app.base import (  # pyright: ignore[reportMissingImports]
            BaseApplication,
        )

        class _StandaloneApplication(BaseApplication):
            def __init__(self, app: Any, options: dict[str, object]):
                self.options = options
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key, value)

            def load(self) -> Any:
                return self.application

        workers = (os.cpu_count() or 1) * 2 + 1
        _StandaloneApplication(
            FlaskApp().app,
            {"bind": f"0.0.0.0:{port}", "workers": workers},
        ).run()
