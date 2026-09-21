from typing import Any, Sequence

from curl_cffi.requests import AsyncSession
from domain.exceptions.web_scraping import NoSuchElementException
from domain.html_elements.interface import HTMLReadingElementInterface
from domain.web_scraping.cookie import Cookie
from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.parser.bs4 import BeautifulSoupParser
from infrastructure.web_scraping.parser.interface import HTMLParserInterface
from infrastructure.web_scraping.parser.selectolax import SelectolaxParser


class CurlCffiAdapter(
    WebScrapingAsyncAdapterBase[HTMLReadingElementInterface]
):
    """Same shape as HTTPXAdapter (fetching and parsing are independent,
    parser is injected), but impersonates a real browser's TLS/JA3
    fingerprint (default: chrome) instead of using a plain HTTP client
    signature — for targets that block httpx/requests by fingerprinting
    the connection itself, not just headers.
    """

    def __init__(self, parser: HTMLParserInterface):
        self.impersonate = "chrome"
        self.client: AsyncSession | None = None
        self.parser = parser
        self.tree: Any = None
        super().__init__()

    async def start(self, *args: Any, **kwargs: Any) -> None:
        await super().start(*args, **kwargs)
        impersonate = kwargs.get("impersonate")
        if isinstance(impersonate, str):
            self.impersonate = impersonate

        self.client = AsyncSession(  # type: ignore
            impersonate=self.impersonate
        )

    async def finish(self):
        if self.client:
            return await self.client.close()

    def _ensure_client(self) -> AsyncSession:
        if not self.client:
            self.client = AsyncSession(  # type: ignore
                impersonate=self.impersonate
            )
        return self.client

    async def open_page(self, url: str):
        self._ensure_client()
        response = await self.client.get(url)
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
        if not self.client:
            return []

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
            for raw in self.client.cookies.jar
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
        if not self.client:
            return {}
        return dict(self.client.headers)

    async def set_headers(self, headers: dict[str, str]) -> None:
        client = self._ensure_client()
        client.headers.update(headers)


class CurlCffiBeautifulSoupAdapter(CurlCffiAdapter):
    def __init__(self):
        super().__init__(BeautifulSoupParser())


class CurlCffiSelectolaxAdapter(CurlCffiAdapter):
    def __init__(self):
        super().__init__(SelectolaxParser())
