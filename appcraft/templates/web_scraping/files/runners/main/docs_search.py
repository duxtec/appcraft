from application.use_cases.web_scraping.docs import SearchDocsUseCase
from domain.exceptions.web_scraping import WebScrapingException
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.provider import (
    TInteractiveAdapter,
    get_default_interactive_adapter,
)
from infrastructure.web_scraping.runner import WebScrapingRunnerBase
from presentation.cli.web_scraping.docs import DocsSearchCLIPresentation


class DocsSearch(Runner, WebScrapingRunnerBase[TInteractiveAdapter]):
    """Searches using whichever interactive (browser) engine is
    installed and configured as the default — config/web_scraping.toml's
    `default_interactive_adapter` picks between selenium/playwright when
    both are installed. There's no per-engine runner to choose between
    instead: code that specifically needs one engine regardless of that
    default should inject its concrete adapter (e.g. `SeleniumAdapter`)
    directly rather than going through this runner — see
    infrastructure/web_scraping/provider.py.
    """

    @property
    def adapter(self) -> TInteractiveAdapter:
        if self._adapter is None:
            adapter = get_default_interactive_adapter()
            if adapter is None:
                raise WebScrapingException(
                    "No interactive (browser) adapter is installed — "
                    "install selenium or playwright first."
                )
            self._adapter = adapter
        return self._adapter

    def __init__(self) -> None:
        search_docs_uc = SearchDocsUseCase(self.adapter)
        self.presentation = DocsSearchCLIPresentation(search_docs_uc)

    @Runner.runner
    def search_template_docs(self, *args: str, **kwargs: str):
        self.start(*args, **kwargs)
        self.presentation.search("Web Scraping")
        self.adapter.finish()
