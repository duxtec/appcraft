from application.schemas.output.app import AppSchema
from application.use_cases.app.get import GetAppUseCase
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
        def app_info(cls, app: AppSchema):
            app_dict = app.model_dump()
            cls.title("App Informations")
            for name, value in app_dict.items():
                cls.info(name, end=": ")
                cls.print(value)

    def __init__(self, app_use_case: GetAppUseCase) -> None:
        self.app_use_case = app_use_case

    def show_informations(self) -> None:
        app = self.app_use_case.execute()
        self.Printer.app_info(app)

    def start(self) -> None:
        app = self.app_use_case.execute()
        self.Printer.welcome(app.name)
