from flask import Flask, render_template
from infrastructure.framework.appcraft.templates.sqlalchemy import (
    SQLAlchemyTemplate,
)
from infrastructure.framework.appcraft.utils.printer import Printer
from infrastructure.framework.flask.router import FlaskRouter
from infrastructure.framework.flask.sqlalchemy import FlaskSQLAlchemy


class FlaskApp:
    def __init__(self):
        configs = {
            "static_folder": "presentation/web/ui/static",
        }

        self.app = Flask(__name__, **configs)

        if SQLAlchemyTemplate.is_installed():
            try:
                FlaskSQLAlchemy(self.app).init_app()
            except Exception as e:
                Printer.error(f"Error connecting to the database: {e}")

        else:
            Printer.warning(
                "\
SQLAlchemy template is not installed, start Flask App without db."
            )

        self.router = FlaskRouter(self.app)

        try:
            self.router.register_api_bp()
        except Exception:
            pass

        try:
            self.router.register_views_bp()
        except Exception:
            pass

        try:
            self.router.register_pages_bp()
        except Exception:
            pass

        @self.app.errorhandler(404)
        def page_not_found(error):
            return render_template("pages/404.html"), 404

        self.show_endpoints()

    def show_endpoints(self):
        Printer.title("Endpoints:")
        for rule in self.app.url_map.iter_rules():
            Printer.info(rule.endpoint, end=": ")
            print(rule.rule)
        print("")
