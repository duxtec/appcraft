import asyncio
from dataclasses import dataclass

from application.ports.web_scraping import WebScrapingAsyncPort
from application.providers.adapters.web_scraping import (
    delegate_to_reading_adapter,
    get_default_interactive_adapter,
)
from application.use_cases import UseCase
from domain.web_scraping.cookie import Cookie


@dataclass
class DelegateSessionInput:
    url: str = "https://httpbin.org/cookies"
    cookie_name: str = "appcraft_demo"
    cookie_value: str = "delegated"


@dataclass
class DelegateSessionResult:
    interactive_adapter_name: str
    reading_adapter_name: str
    session_copied: bool
    cookies_before: list[Cookie]
    cookies_after: list[Cookie]


class DelegateSessionUseCase(
    UseCase[DelegateSessionInput, DelegateSessionResult]
):
    """Example: does the part of the flow that needs a real browser
    (here, just setting a cookie — stand-in for a login/JS challenge)
    on the default interactive adapter, then delegates the rest to the
    default reading adapter, carrying the session over automatically
    (or just continuing on the same adapter, if no faster one is
    installed — see delegate_to_reading_adapter()).

    Confirms the handoff by comparing each adapter's own get_cookies()
    before/after, rather than fetching and parsing the page's response
    body: url defaults to an endpoint that returns plain JSON, and
    BeautifulSoup's html.parser backend (unlike selectolax) doesn't
    synthesize a <body> for content with no actual HTML tags, so a
    selector-based check would only work with some parser/URL
    combinations.
    """

    def execute(
        self, input_data: DelegateSessionInput
    ) -> DelegateSessionResult:
        return asyncio.run(self._execute_async(input_data))

    async def _execute_async(
        self, input_data: DelegateSessionInput
    ) -> DelegateSessionResult:
        interactive = get_default_interactive_adapter()
        if interactive is None:
            raise RuntimeError(
                "No interactive (browser) adapter installed — add "
                "selenium or playwright first."
            )
        interactive_name = type(interactive).__name__
        cookie = Cookie(
            name=input_data.cookie_name, value=input_data.cookie_value
        )

        if isinstance(interactive, WebScrapingAsyncPort):
            await interactive.start(headless=True)
            await interactive.open_page(input_data.url)
            await interactive.set_cookies([cookie])
            cookies_before = await interactive.get_cookies()
        else:
            interactive.start(headless=True)
            interactive.open_page(input_data.url)
            interactive.set_cookies([cookie])
            cookies_before = interactive.get_cookies()

        reading = await delegate_to_reading_adapter(interactive)
        session_copied = reading is not interactive
        reading_name = type(reading).__name__

        if isinstance(reading, WebScrapingAsyncPort):
            await reading.open_page(input_data.url)
            cookies_after = await reading.get_cookies()
            await reading.finish()
        else:
            reading.open_page(input_data.url)
            cookies_after = reading.get_cookies()
            reading.finish()

        return DelegateSessionResult(
            interactive_adapter_name=interactive_name,
            reading_adapter_name=reading_name,
            session_copied=session_copied,
            cookies_before=cookies_before,
            cookies_after=cookies_after,
        )
