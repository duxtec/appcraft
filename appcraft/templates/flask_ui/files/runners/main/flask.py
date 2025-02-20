from infrastructure.framework.appcraft.core.app_runner import AppRunner
from infrastructure.framework.flask.app import FlaskApp


class Flask(AppRunner):
    @AppRunner.runner
    def start(self):
        FlaskApp().app.run(debug=True)

    def non_runner1(self):
        # This method does not show in the runner.
        pass
