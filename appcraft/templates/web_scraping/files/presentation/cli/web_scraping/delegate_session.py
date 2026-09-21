from application.use_cases.web_scraping.delegate_session import (
    DelegateSessionInput,
    DelegateSessionResult,
    DelegateSessionUseCase,
)
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class DelegateSessionCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "delegate_session"

        @classmethod
        def show(cls, result: DelegateSessionResult):
            cls.title("Session delegation demo")
            cls.info("Interactive adapter", end=": ")
            print(result.interactive_adapter_name)
            cls.info("Reading adapter", end=": ")
            print(result.reading_adapter_name)
            cls.info("Session copied", end=": ")
            print(result.session_copied)
            print()
            cls.title("Cookies seen by the interactive adapter")
            for cookie in result.cookies_before:
                print(f"  {cookie.name} = {cookie.value}")
            cls.title("Cookies seen by the reading adapter, after handoff")
            for cookie in result.cookies_after:
                print(f"  {cookie.name} = {cookie.value}")

    def __init__(self, delegate_session_uc: DelegateSessionUseCase) -> None:
        self.delegate_session_uc = delegate_session_uc

    def run(self, input_data: DelegateSessionInput) -> None:
        result = self.delegate_session_uc.execute(input_data)
        self.Printer.show(result)
