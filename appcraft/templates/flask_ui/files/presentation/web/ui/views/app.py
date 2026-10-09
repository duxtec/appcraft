from flask import render_template

from infrastructure.app.adapter import AppAdapter


def app():
    app = AppAdapter().get()
    return render_template(
        "views/app.html",
        app_name=app.name,
        version=app.version,
        debug_mode=app.debug_mode,
        environment=app.environment.value,
    )
