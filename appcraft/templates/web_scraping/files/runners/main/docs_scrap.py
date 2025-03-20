from abc import ABC

from application.services.web_scraping.docs import DocScrapService
from infrastructure.framework.appcraft.core.app_runner import (
    AppRunnerInterface,
)
from infrastructure.web_scraping.adapters.playwright import PlaywrightAdapter
from infrastructure.web_scraping.adapters.selenium import SeleniumAdapter
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingAdapterInteractive,
)
from presentation.cli.web_scraping.docs import DocScrapPresenter
from runners.main.scrapping import RunnerScrap


class DocScrap(RunnerScrap[TWebScrapingAdapterInteractive], ABC):
    def __init__(self) -> None:
        self.service = DocScrapService(self.adapter)
        self.presenter = DocScrapPresenter(self.service)

    @AppRunnerInterface.runner
    def search_template_docs(self, *args: str, **kwargs: str):
        self.start(*args, **kwargs)
        results = self.service.search("Web Scraping")
        self.presenter.show_search_results(results)
        self.adapter.finish()


class Selenium(AppRunnerInterface, DocScrap[SeleniumAdapter]):
    pass


class Playwright(AppRunnerInterface, DocScrap[PlaywrightAdapter]):
    pass
