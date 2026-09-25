import asyncio

from application.use_cases.web_scraping.page_info import GetPageLinksUseCase
from domain.exceptions.web_scraping import WebScrapingException
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.provider import (
    TReadingAdapter,
    get_default_reading_adapter,
)
from infrastructure.web_scraping.runner import WebScrapingRunnerBase
from presentation.cli.web_scraping.page_info import PageLinksCLIPresentation


class PageLinks(Runner, WebScrapingRunnerBase[TReadingAdapter]):
    """Extracts links using whichever engine is installed and configured
    as the default reading (non-interactive) adapter — config/
    web_scraping.toml's `default_reading_adapter` picks between httpx/
    curl_cffi when more than one is installed, falling back to the
    default interactive (browser) engine if neither is. There's no
    per-engine runner to choose between instead: code that specifically
    needs one engine regardless of that default should inject its
    concrete adapter (e.g. `HTTPXSelectolaxAdapter`) directly rather
    than going through this runner — see
    infrastructure/web_scraping/provider.py.
    """

    @property
    def adapter(self) -> TReadingAdapter:
        if self._adapter is None:
            adapter = get_default_reading_adapter()
            if adapter is None:
                raise WebScrapingException(
                    "No web scraping adapter is installed — install "
                    "selenium, playwright, httpx, or curl_cffi first."
                )
            self._adapter = adapter
        return self._adapter

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
