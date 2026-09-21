from abc import ABC, abstractmethod
from typing import Any

from domain.html_elements.interface import HTMLReadingElementInterface


class HTMLParserInterface(ABC):
    """Parses raw HTML text into a tree and queries it — the piece that
    varies independently of *how* the HTML was fetched (httpx, curl_cffi,
    ...), so adapters take one of these instead of hardcoding a parser.
    """

    @abstractmethod
    def parse(self, text: str) -> Any: ...

    @abstractmethod
    def select_one(
        self, tree: Any, selector: str
    ) -> HTMLReadingElementInterface | None: ...

    @abstractmethod
    def select_all(
        self, tree: Any, selector: str
    ) -> list[HTMLReadingElementInterface]: ...
