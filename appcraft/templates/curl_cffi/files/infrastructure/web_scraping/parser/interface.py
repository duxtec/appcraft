from abc import ABC, abstractmethod
from typing import Any

from domain.html_elements.interface import HTMLReadingElement


class HTMLParser(ABC):
    """Parses raw HTML text into a tree and queries it — the piece that
    varies independently of *how* the HTML was fetched (httpx, curl_cffi,
    ...), so adapters take one of these instead of hardcoding a parser.
    """

    @abstractmethod
    def parse(self, text: str) -> Any: ...

    @abstractmethod
    def select_one(
        self, tree: Any, selector: str
    ) -> HTMLReadingElement | None: ...

    @abstractmethod
    def select_all(
        self, tree: Any, selector: str
    ) -> list[HTMLReadingElement]: ...
