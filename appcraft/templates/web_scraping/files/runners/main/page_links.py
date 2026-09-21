import asyncio
from abc import ABC

from application.use_cases.web_scraping.page_info import GetPageLinksUseCase
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.runner import WebScrapingRunnerBase
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingSyncOrAsyncAdapterReading,
)
from presentation.cli.web_scraping.page_info import PageLinksCLIPresentation


class PageLinksRunnerBase(
    WebScrapingRunnerBase[TWebScrapingSyncOrAsyncAdapterReading], ABC
):
    """Abstract runner mixin — subclass per adapter, e.g.:
    `class HTTPXBeautifulSoup(PageLinksRunnerBase[HTTPXBeautifulSoupAdapter], Runner): pass`
    (see the selenium/playwright/httpx/curl_cffi templates' own
    runners/main files).
    """

    def __init__(self) -> None:
        get_page_links_uc = GetPageLinksUseCase(self.adapter)
        self.presentation = PageLinksCLIPresentation(get_page_links_uc)

    @Runner.runner
    def get_links(
        self,
        *args: str,
        **kwargs: str,
    ):
        self.start(*args, **kwargs)
        urls = kwargs.get("urls")
        if urls:
            urls_list = urls.split(" ")
        else:
            urls_list = [arg for arg in args if not str(arg).startswith("-")]

        self.presentation.show_links(urls_list)

        if isinstance(self.adapter, WebScrapingAsyncAdapterBase):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.create_task(self.adapter.finish())
        else:
            self.adapter.finish()
