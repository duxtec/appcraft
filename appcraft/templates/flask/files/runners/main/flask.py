from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.framework.flask.app import FlaskApp


class Flask(Runner):
    @Runner.runner
    def start(self):
        FlaskApp().app.run(debug=True)
        return False
