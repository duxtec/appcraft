import inspect
import os
from typing import cast

from flask import Blueprint, Flask, Response, render_template
from jinja2 import FileSystemLoader

from infrastructure.framework.appcraft.utils.import_manager import (
    ImportManager,
)


class FlaskRouter:
    def __init__(self, app: Flask) -> None:
        self.app = app

        self.loader = cast(FileSystemLoader, self.app.jinja_loader)

        self.templates_path = os.path.abspath(
            os.path.join(
                "presentation",
                "web",
                "ui",
                "templates",
            )
        )

        @self.app.after_request
        def after_request(  # pyright: ignore[reportUnusedFunction]
            response: Response,
        ) -> Response:
            if response.content_type == "application/json":
                response.headers["Content-Type"] = (
                    "application/json; charset=utf-8"
                )
            return response

    def register_api_bp(self):
        v1_bp = Blueprint("v1", __name__, url_prefix="/v1")
        v1_attributes = ImportManager(
            "presentation.web.api.v1.routes"
        ).get_module_attributes()

        for _, module in v1_attributes.items():
            for _, attr in module.items():
                if isinstance(attr, Blueprint):
                    v1_bp.register_blueprint(attr)
                elif inspect.isfunction(attr) and attr.__name__ == "register":
                    bp = attr()
                    if isinstance(bp, Blueprint):
                        v1_bp.register_blueprint(bp)

        api_bp = Blueprint("api", __name__, url_prefix="/api")
        api_bp.register_blueprint(v1_bp)

        self.app.register_blueprint(api_bp)

    def register_views_bp(self):
        self.loader.searchpath.append(self.templates_path)

        views_bp = Blueprint("views", __name__, url_prefix="")

        views_modules = ImportManager(
            "presentation.web.ui.views"
        ).get_module_attributes()

        for _, module in views_modules.items():
            for attr_name, attr in module.items():
                if inspect.isfunction(attr):
                    attr_name = "" if attr_name == "index" else attr_name

                views_bp.add_url_rule(
                    f"/{attr_name}",
                    attr_name,
                    attr,
                )

        self.app.register_blueprint(views_bp)

    def register_pages_bp(self):
        self.loader.searchpath.append(self.templates_path)

        pages_bp = Blueprint("pages", __name__, url_prefix="")

        for filename in os.listdir(
            os.path.join(self.templates_path, "pages")
        ):
            if filename.endswith(".html"):
                route_name = filename.replace(".html", "")
                route_name = "" if route_name == "index" else route_name

                # Use route_name as the explicit endpoint to avoid collisions,
                # since every view function is otherwise named "render_page"
                endpoint_name = route_name or "index"

                def render_page(filename: str = filename):
                    return render_template(f"pages/{filename}")

                pages_bp.add_url_rule(
                    f"/{route_name}",
                    endpoint=endpoint_name,
                    view_func=render_page,
                )

        self.app.register_blueprint(pages_bp)
