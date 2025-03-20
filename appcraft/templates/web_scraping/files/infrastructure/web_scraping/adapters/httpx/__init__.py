from abc import ABC, abstractmethod
from typing import Any

import httpx

from infrastructure.web_scraping.adapters.base import (
    WebScrapingAsyncAdapterBase,
)
from infrastructure.web_scraping.types.html_elements import (
    THTMLReadingElement,
)


class HTTPXAdapter(WebScrapingAsyncAdapterBase[THTMLReadingElement], ABC):
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.tree = None

    async def start(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def finish(self):
        return await self.client.aclose()

    async def open_page(self, url: str):
        response = await self.client.get(url)
        response.raise_for_status()
        self.tree = await self.html_parser(response.text)

    @abstractmethod
    async def html_parser(self, text: str) -> Any: ...
