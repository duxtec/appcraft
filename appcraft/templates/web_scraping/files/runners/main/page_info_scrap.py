import asyncio
from abc import ABC

from application.services.web_scraping.page_info import PageInfoScrapService
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.web_scraping.adapters.base import (
    WebScrapingAsyncAdapterBase,
)
from infrastructure.web_scraping.adapters.httpx.bs4 import (
    HTTPXBeautifulSoupAdapter,
)
from infrastructure.web_scraping.adapters.httpx.selectolax import (
    HTTPXSelectolaxAdapter,
)
from infrastructure.web_scraping.adapters.playwright import PlaywrightAdapter
from infrastructure.web_scraping.adapters.selenium import SeleniumAdapter
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingSyncOrAsyncAdapterReading,
)
from presentation.cli.web_scraping.page_info import PageInfoScrapPresenter
from runners.main.scrapping import RunnerScrap


class PageInfoScrap(RunnerScrap[TWebScrapingSyncOrAsyncAdapterReading], ABC):
    def __init__(self) -> None:
        self.service = PageInfoScrapService(self.adapter)
        self.presenter = PageInfoScrapPresenter(self.service)

    @AppRunnerInterface.runner
    def get_links(
        self,
        *args: str,
        **kwargs: str,
    ):
        self.start(*args, **kwargs)
        urls = kwargs.get("urls")
        if urls:
            urls = urls.split(" ")
        else:
            urls = [arg for arg in args if not str(arg).startswith("-")]

        links = self.service.get_links(urls)
        self.presenter.show_links(links)

        if isinstance(self.adapter, WebScrapingAsyncAdapterBase):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.create_task(self.adapter.finish())
        else:
            self.adapter.finish()


class Selenium(PageInfoScrap[SeleniumAdapter], AppRunnerInterface):
    pass


class Playwright(PageInfoScrap[PlaywrightAdapter], AppRunnerInterface):
    pass


class HTTPXSelectolax(
    PageInfoScrap[HTTPXSelectolaxAdapter], AppRunnerInterface
):
    pass


class HTTPXBeautifulSoup(
    PageInfoScrap[HTTPXBeautifulSoupAdapter], AppRunnerInterface
):
    pass
