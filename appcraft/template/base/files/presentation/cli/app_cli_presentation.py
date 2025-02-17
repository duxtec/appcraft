from application.services.app_service import AppService
from domain.models.app import App
from infrastructure.framework.appcraft.utils.component_printer \
    import ComponentPrinter


class AppCLIPresentation():
    class Printer(ComponentPrinter):
        domain = "app"

        @classmethod
        def welcome(cls, app_name):
            message = cls.translate("Welcome to {app_name}")
            cls.title(message.format(app_name=app_name))

        @classmethod
        def app_info(cls, app: App):
            cls.title("App Informations")
            cls.info("Name", end=": ")
            cls.print(app.name)
            cls.info("Language", end=": ")
            cls.print(app.language)
            cls.info("Version", end=": ")
            cls.print(app.version)
            cls.info("Environment", end=": ")
            cls.print(app.environment)
            cls.info("Debug Mode", end=": ")
            cls.print(app.debug_mode)
            cls.info("Log Level", end=": ")
            cls.print(app.log_level)
            cls.info("Supported Languages", end=": ")
            cls.print(", ".join(app.supported_languages))

    def show_informations(self):
        service = AppService()
        app = service.get_app()
        self.Printer.app_info(app)

    def start(self):
        service = AppService()
        app = service.get_app()
        self.Printer.welcome(app.name)
