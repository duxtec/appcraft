from abc import ABC
from typing import Any, Generic

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from domain.web_scraping.session import WebScrapingSession
from infrastructure.web_scraping.types.html_elements import THTMLElement


class WebScrapingAdapterBase(
    WebScrapingPort[THTMLElement],
    ABC,
    Generic[THTMLElement],
):

    def start(self, *args: Any, **kwargs: Any) -> None:
        headless = kwargs.get("headless")
        timeout = kwargs.get("timeout")
        self.headless = headless if isinstance(headless, bool) else False
        self.timeout = timeout if isinstance(timeout, float) else self.timeout

    def __init__(self):
        self.headless = False
        self.timeout = 5

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        self._timeout = value

    def get_session(self) -> WebScrapingSession:
        """Cookies + headers together, in one call — hand the whole
        thing to another adapter with set_session() instead of copying
        each piece separately.
        """
        return WebScrapingSession(
            cookies=self.get_cookies(), headers=self.get_headers()
        )

    def set_session(self, session: WebScrapingSession) -> None:
        self.set_cookies(session.cookies)
        self.set_headers(session.headers)


class WebScrapingAsyncAdapterBase(
    WebScrapingAsyncPort[THTMLElement],
    ABC,
    Generic[THTMLElement],
):

    async def start(self, *args: Any, **kwargs: Any):
        headless = kwargs.get("headless")
        timeout = kwargs.get("timeout")
        self.headless = headless if isinstance(headless, bool) else False
        self.timeout = timeout if isinstance(timeout, float) else self.timeout

    def __init__(self):
        self.headless = False
        self.timeout = 5

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        self._timeout = value

    async def get_session(self) -> WebScrapingSession:
        """Cookies + headers together, in one call — hand the whole
        thing to another adapter with set_session() instead of copying
        each piece separately.
        """
        return WebScrapingSession(
            cookies=await self.get_cookies(),
            headers=await self.get_headers(),
        )

    async def set_session(self, session: WebScrapingSession) -> None:
        await self.set_cookies(session.cookies)
        await self.set_headers(session.headers)
