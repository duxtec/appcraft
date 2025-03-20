from abc import ABC, abstractmethod
from typing import Any, Generic

from application.interfaces.adapters import AdapterInterface
from infrastructure.web_scraping.types.html_elements import THTMLElement


class WebScrapingAdapterInterface(
    AdapterInterface, ABC, Generic[THTMLElement]
):
    @abstractmethod
    def start(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def finish(self) -> None:
        pass

    @abstractmethod
    def open_page(self, url: str) -> None:
        pass

    @abstractmethod
    def query_selector(self, selector: str) -> THTMLElement:
        pass

    @abstractmethod
    def query_selector_all(self, selector: str) -> list[THTMLElement]:
        pass


class WebScrapingAsyncAdapterInterface(
    AdapterInterface, ABC, Generic[THTMLElement]
):
    @abstractmethod
    async def start(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    async def finish(self) -> None:
        pass

    @abstractmethod
    async def open_page(self, url: str) -> None:
        pass

    @abstractmethod
    async def query_selector(self, selector: str) -> THTMLElement:
        pass

    @abstractmethod
    async def query_selector_all(self, selector: str) -> list[THTMLElement]:
        pass
