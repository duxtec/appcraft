from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import NotFound

from infrastructure.framework.appcraft.core.config import Config
from infrastructure.framework.appcraft.templates.flask_api import (
    FlaskAPITemplate,
)
from infrastructure.framework.appcraft.templates.flask_ui import (
    FlaskUITemplate,
)
from infrastructure.framework.appcraft.templates.sqlalchemy import (
    SQLAlchemyTemplate,
)
from infrastructure.framework.appcraft.utils.color import Color
from infrastructure.framework.appcraft.utils.printer import Printer
from infrastructure.framework.flask.router import FlaskRouter


class FlaskApp:
    def __init__(self):
        project_root = Path.cwd()

        configs: dict[str, Any] = {
            "static_folder": project_root
            / "presentation"
            / "web"
            / "ui"
            / "static",
        }

        self.app = Flask(__name__, **configs)

        @self.app.context_processor
        def inject_palette():  # pyright: ignore[reportUnusedFunction]
            return {"palette": Color.palette()}

        @self.app.context_processor
        def inject_globals() -> (  # pyright: ignore[reportUnusedFunction]
            dict[str, Any]
        ):
            app_name: str = Config().get("app")["name"]
            current_year: int = datetime.now().year

            return {
                "app_name": app_name,
                "current_year": current_year,
            }

        if SQLAlchemyTemplate.is_installed():
            try:
                from infrastructure.framework.flask.sqlalchemy import (
                    FlaskSQLAlchemy,
                )

                FlaskSQLAlchemy(self.app).init_app()
            except Exception as e:
                Printer.error(f"Error connecting to the database: {e}")

        else:
            Printer.warning("\
SQLAlchemy template is not installed, start Flask App without db.")

        self.router = FlaskRouter(self.app)

        if FlaskAPITemplate.is_installed():
            self.router.register_api_bp()

        if FlaskUITemplate.is_installed():
            self.router.register_views_bp()
            self.router.register_pages_bp()

        @self.app.errorhandler(404)
        def page_not_found(error: NotFound):  # type: ignore
            if FlaskAPITemplate.is_installed():
                if (
                    request.path.startswith("/api")
                    or not FlaskUITemplate.is_installed()
                ):
                    return (
                        jsonify(
                            {"error": "Not Found", "message": str(error)}
                        ),
                        404,
                    )
            return render_template("pages/404.html"), 404

        self.show_endpoints()

    def show_endpoints(self):
        Printer.title("Endpoints:")
        for rule in self.app.url_map.iter_rules():
            Printer.info(rule.endpoint, end=": ")
            print(rule.rule)
        print("")
