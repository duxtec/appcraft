from core.app import App
from core.flask.app import create_app
class Server(App):
    
    
    @App.runner
    def start(self):
        app = create_app()
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
