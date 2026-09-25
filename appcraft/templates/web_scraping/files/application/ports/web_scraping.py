from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence

from application.ports import Port
from domain.types.html_elements import THTMLElement
from domain.web_scraping.cookie import Cookie


class WebScrapingPort(Port, ABC, Generic[THTMLElement]):
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

    @abstractmethod
    def get_cookies(self) -> list[Cookie]:
        pass

    @abstractmethod
    def set_cookies(self, cookies: Sequence[Cookie]) -> None:
        pass

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        pass

    @abstractmethod
    def set_headers(self, headers: dict[str, str]) -> None:
        pass


class WebScrapingAsyncPort(Port, ABC, Generic[THTMLElement]):
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

    @abstractmethod
    async def get_cookies(self) -> list[Cookie]:
        pass

    @abstractmethod
    async def set_cookies(self, cookies: Sequence[Cookie]) -> None:
        pass

    @abstractmethod
    async def get_headers(self) -> dict[str, str]:
        pass

    @abstractmethod
    async def set_headers(self, headers: dict[str, str]) -> None:
        pass
