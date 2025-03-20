from abc import ABC
from typing import Any

from playwright.sync_api import Browser, BrowserType, sync_playwright

from infrastructure.web_scraping.adapters.base import WebScrapingAdapterBase
from infrastructure.web_scraping.exceptions import NoSuchElementException
from infrastructure.web_scraping.html_elements.playwright import (
    PlaywrightHTMLElement,
)


class PlaywrightAdapter(WebScrapingAdapterBase[PlaywrightHTMLElement], ABC):
    def __init__(self):
        self._browser: Browser | None = None
        self._playwright = sync_playwright().start()
        self.page = None
        super().__init__()

    @property
    def browser(self) -> Browser:
        if self._browser:
            return self._browser

        self._browser = self._playwright.chromium.launch(
            headless=self._headless
        )
        return self._browser

    @browser.setter
    def browser(self, browser: BrowserType):
        self._browser = browser.launch(headless=self.headless)

    def start(self, *args: Any, **kwargs: Any):
        super().start(*args, **kwargs)
        self.browser = self._playwright.chromium
        self.page = self.browser.new_page()

    def finish(self):
        """Closes the Playwright browser session."""
        if self.browser:
            self.browser.close()

    def open_page(self, url: str):
        """Opens the specified URL in the browser."""
        if self.page:
            self.page.goto(url, timeout=self._timeout * 1000)

    def query_selector(self, selector: str) -> PlaywrightHTMLElement:
        """Finds a single element by the CSS selector."""
        if self.page:
            element = self.page.query_selector(selector)
            if element:
                return PlaywrightHTMLElement(element, self.page)
        raise NoSuchElementException()

    def query_selector_all(
        self, selector: str
    ) -> list[PlaywrightHTMLElement]:
        """Finds all elements matching the CSS selector."""
        if self.page:
            self.page.wait_for_selector(selector, timeout=self.timeout * 1000)
            elements = self.page.query_selector_all(selector)
            return [PlaywrightHTMLElement(el, self.page) for el in elements]
        return []
