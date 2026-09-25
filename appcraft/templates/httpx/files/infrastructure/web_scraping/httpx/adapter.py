from typing import Any, Sequence

import httpx
from domain.exceptions.web_scraping import NoSuchElementException
from domain.html_elements.interface import HTMLReadingElementInterface
from domain.web_scraping.cookie import Cookie
from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.parser.bs4 import BeautifulSoupParser
from infrastructure.web_scraping.parser.interface import HTMLParserInterface
from infrastructure.web_scraping.parser.selectolax import SelectolaxParser


class HTTPXAdapter(WebScrapingAsyncAdapterBase[HTMLReadingElementInterface]):
    """Fetching (httpx) is independent of parsing — pass whichever
    HTMLParserInterface the target page calls for. HTTPXBeautifulSoupAdapter
    / HTTPXSelectolaxAdapter below are just that, pre-wired, so the
    generic web_scraping runner mixins (which construct adapters with no
    arguments) have a concrete, zero-arg class to instantiate.
    """

    def __init__(self, parser: HTMLParserInterface):
        self.client: httpx.AsyncClient | None = None
        self.parser = parser
        self.tree: Any = None
        super().__init__()

    def _ensure_client(self) -> httpx.AsyncClient:
        # Created lazily rather than in __init__, matching
        # CurlCffiAdapter's own pattern, so a fresh adapter built in a
        # plain sync context (no event loop running yet) doesn't try to
        # construct it before one exists.
        if self.client is None:
            self.client = httpx.AsyncClient()
        return self.client

    async def start(self, *args: Any, **kwargs: Any) -> None:
        self._ensure_client()

    async def finish(self):
        if self.client is None:
            return
        try:
            await self.client.aclose()
        except RuntimeError:
            # start()/open_page()/finish() each run under their own
            # asyncio.run() call when driven from synchronous code (a
            # runner, or the benchmark tool) — httpx.AsyncClient's
            # connection pool binds to whichever loop is running the
            # first time it's actually used, so closing it from a later,
            # different loop raises "Event loop is closed" even though
            # the connection itself is already gone along with that
            # loop. Nothing left to clean up in that case.
            pass
        finally:
            self.client = None

    async def open_page(self, url: str):
        response = await self._ensure_client().get(url)
        response.raise_for_status()
        self.tree = self.parser.parse(response.text)

    async def query_selector(
        self, selector: str
    ) -> HTMLReadingElementInterface:
        if self.tree is None:
            raise NoSuchElementException()

        element = self.parser.select_one(self.tree, selector)
        if element is None:
            raise NoSuchElementException()

        return element

    async def query_selector_all(
        self, selector: str
    ) -> list[HTMLReadingElementInterface]:
        if self.tree is None:
            return []

        return self.parser.select_all(self.tree, selector)

    async def get_cookies(self) -> list[Cookie]:
        return [
            Cookie(
                name=raw.name,
                value=raw.value or "",
                domain=raw.domain or None,
                path=raw.path or "/",
                secure=bool(raw.secure),
                http_only=bool(raw.get_nonstandard_attr("HttpOnly")),
                expires=raw.expires,
            )
            for raw in self._ensure_client().cookies.jar
        ]

    async def set_cookies(self, cookies: Sequence[Cookie]) -> None:
        client = self._ensure_client()
        for cookie in cookies:
            client.cookies.set(
                cookie.name,
                cookie.value,
                domain=cookie.domain or "",
                path=cookie.path,
            )

    async def get_headers(self) -> dict[str, str]:
        return dict(self._ensure_client().headers)

    async def set_headers(self, headers: dict[str, str]) -> None:
        self._ensure_client().headers.update(headers)


class HTTPXBeautifulSoupAdapter(HTTPXAdapter):
    def __init__(self):
        super().__init__(BeautifulSoupParser())


class HTTPXSelectolaxAdapter(HTTPXAdapter):
    def __init__(self):
        super().__init__(SelectolaxParser())
