from flask import render_template
from application.services.app_service import AppService
from domain.models.app import App


def app():
    app: App = AppService().get_app()
    return render_template(
        "views/app.html",
        app_name=app.name,
        version=app.version,
        debug_mode=app.debug_mode,
        log_level=app.log_level,
        environment=app.environment,
    )
