from abc import ABC, abstractmethod
from typing import Any, Generic

from application.interfaces.adapters import AdapterInterface
from infrastructure.web_scraping.interfaces.adapters import THTMLElement


class WebScrapingAsyncAdapterInterface(
    AdapterInterface, ABC, Generic[THTMLElement]
):
    @abstractmethod
    async def start(self, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    async def finish(self):
        pass

    @abstractmethod
    async def open_page(self, url: str):
        pass

    @abstractmethod
    async def query_selector(self, selector: str) -> THTMLElement:
        pass

    @abstractmethod
    async def query_selector_all(self, selector: str) -> list[THTMLElement]:
        pass
