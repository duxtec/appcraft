from flask import render_template

from infrastructure.framework.appcraft.app.provider import AppProvider


def app():
    app = AppProvider().get()
    return render_template(
        "views/app.html",
        app_name=app.name,
        version=app.version,
        debug_mode=app.debug_mode,
        environment=app.environment,
    )
