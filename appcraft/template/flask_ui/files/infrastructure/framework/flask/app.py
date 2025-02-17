import inspect
import os
from infrastructure.framework.flask.router import FlaskRouter
from flask import Flask, Blueprint, render_template
from infrastructure.framework.appcraft.utils.import_manager \
    import ImportManager
from infrastructure.framework.appcraft.utils.printer import Printer


class FlaskApp:
    def __init__(self):
        configs = {
            "static_folder": 'presentation/web/ui/static',
        }
        if True: # config and 'SQLALCHEMY_DATABASE_URI' in config:
            self.app = Flask(__name__, **configs)
        else:
            pass # self.app = database_app(app)
        
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
