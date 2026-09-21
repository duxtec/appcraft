from abc import ABC

from application.use_cases.web_scraping.docs import SearchDocsUseCase
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.runner import WebScrapingInteractiveRunnerBase
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingAdapterInteractive,
)
from presentation.cli.web_scraping.docs import DocsSearchCLIPresentation


class DocsSearchRunnerBase(
    WebScrapingInteractiveRunnerBase[TWebScrapingAdapterInteractive], ABC
):
    """Abstract runner mixin — subclass per adapter, e.g.:
    `class Selenium(Runner, DocsSearchRunnerBase[SeleniumAdapter]): pass`
    (see the selenium/playwright templates' own runners/main files).
    """

    def __init__(self) -> None:
        search_docs_uc = SearchDocsUseCase(self.adapter)
        self.presentation = DocsSearchCLIPresentation(search_docs_uc)

    @Runner.runner
    def search_template_docs(self, *args: str, **kwargs: str):
        self.start(*args, **kwargs)
        self.presentation.search("Web Scraping")
        self.adapter.finish()
