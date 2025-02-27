from application.dtos.app_dto import AppDTO
from application.services.app_service import AppService
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class AppCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "app"

        @classmethod
        def welcome(cls, app_name: str):
            message = cls.translate("Welcome to {app_name}")
            cls.title(message.format(app_name=app_name))

        @classmethod
        def app_info(cls, app: AppDTO):
            app_dict = app.to_dict()
            cls.title("App Informations")
            for name, value in app_dict.items():
                cls.info(name, end=": ")
                cls.print(value)

    def __init__(self, app_service: AppService) -> None:
        self.app_service = app_service

    def show_informations(self) -> None:
        app = self.app_service.get_app()
        self.Printer.app_info(app)

    def start(self) -> None:
        app = self.app_service.get_app()
        self.Printer.welcome(app.name)
