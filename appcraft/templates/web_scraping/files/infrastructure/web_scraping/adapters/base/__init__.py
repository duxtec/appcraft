from abc import ABC
from typing import Any, Generic

from infrastructure.web_scraping.interfaces.adapters import (
    WebScrapingAdapterInterface,
    WebScrapingAsyncAdapterInterface,
)
from infrastructure.web_scraping.types.html_elements import THTMLElement


class WebScrapingAdapterBase(
    WebScrapingAdapterInterface[THTMLElement],
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


class WebScrapingAsyncAdapterBase(
    WebScrapingAsyncAdapterInterface[THTMLElement],
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
