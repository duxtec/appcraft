from application.use_cases.web_scraping.delegate_session import (
    DelegateSessionInput,
    DelegateSessionUseCase,
)
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.web_scraping.delegate_session import (
    DelegateSessionCLIPresentation,
)


class DelegateSession(Runner):
    @Runner.runner
    def run(
        self,
        url: str | None = None,
        cookie_name: str | None = None,
        cookie_value: str | None = None,
    ):
        input_data = DelegateSessionInput()
        if url:
            input_data.url = url
        if cookie_name:
            input_data.cookie_name = cookie_name
        if cookie_value:
            input_data.cookie_value = cookie_value

        presentation = DelegateSessionCLIPresentation(DelegateSessionUseCase())
        presentation.run(input_data)
