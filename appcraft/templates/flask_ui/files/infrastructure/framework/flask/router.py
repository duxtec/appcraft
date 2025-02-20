import inspect
import os
from flask import Blueprint, render_template

from infrastructure.framework.appcraft.utils.import_manager import ImportManager


class FlaskRouter():
    def __init__(self, app) -> None:
        self.app = app
        
        self.templates_path = os.path.abspath(
            os.path.join(
                'presentation', 'web', 'ui', 'templates',
            )
        )
        
        @self.app.after_request
        def after_request(response):
            if response.content_type == 'application/json':
                response.charset = 'utf-8'
            return response

    def register_api_bp(self):
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        api_attributes = ImportManager(
            "presentation.web.api"
        ).get_module_attributes()
        for name, attr in api_attributes.items():
            api_bp.register_blueprint(attr, url_prefix=f'/{name}')

        self.app.register_blueprint(api_bp)

    def register_views_bp(self):
        self.app.jinja_loader.searchpath.append(self.templates_path)

        views_bp = Blueprint('views', __name__, url_prefix='')
        views_modules = ImportManager(
            "presentation.web.ui.views"
        ).get_module_attributes()
        
        
        for module_name, module in views_modules.items():
            for attr_name, attr in module.items():
                if inspect.isfunction(attr):
                    attr_name = "" if attr_name == "index" else attr_name

                views_bp.add_url_rule(f'/{attr_name}', attr_name, attr)
        self.app.register_blueprint(views_bp)

    def register_pages_bp(self):
        self.app.jinja_loader.searchpath.append(self.templates_path)
        pages_bp = Blueprint('pages', __name__, url_prefix='')

        for filename in os.listdir(
            os.path.join(self.templates_path, "pages")
        ):
            if filename.endswith('.html'):
                route_name = filename.replace('.html', '')

                route_name = "" if route_name == "index" else route_name

                @pages_bp.route(f'/{route_name}')
                def render_page(
                    route_name=route_name, filename=filename
                ):
                    return render_template(f"pages/{filename}")

        self.app.register_blueprint(pages_bp)