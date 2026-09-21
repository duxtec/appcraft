from abc import ABC
from typing import Any, Sequence

from domain.exceptions.web_scraping import NoSuchElementException
from domain.web_scraping.cookie import Cookie
from infrastructure.web_scraping.adapter import WebScrapingAdapterBase
from infrastructure.web_scraping.playwright.html_element import (
    PlaywrightHTMLElement,
)
from playwright.sync_api import Browser, BrowserType, sync_playwright


class PlaywrightAdapter(WebScrapingAdapterBase[PlaywrightHTMLElement], ABC):
    def __init__(self):
        self._browser: Browser | None = None
        self._playwright = sync_playwright().start()
        self.page = None
        # Playwright's own set_extra_http_headers() replaces the whole
        # extra-headers dict rather than merging into it, and there's no
        # get_extra_http_headers() to read it back — tracked here so
        # both get_headers() and repeated set_headers() calls behave.
        self._headers: dict[str, str] = {}
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
            self._browser = None

        # Without stopping the driver connection too, a second
        # PlaywrightAdapter created later in the same process (e.g. the
        # web_scraping benchmark's runs=N loop) trips Playwright's own
        # "sync API already in use" guard.
        self._playwright.stop()

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

    def get_cookies(self) -> list[Cookie]:
        if not self.page:
            return []

        return [
            Cookie(
                name=raw["name"],
                value=raw["value"],
                domain=raw.get("domain"),
                path=raw.get("path", "/"),
                secure=raw.get("secure", False),
                http_only=raw.get("httpOnly", False),
                expires=(
                    raw["expires"]
                    if raw.get("expires", -1) != -1
                    else None
                ),
                same_site=raw.get("sameSite"),
            )
            for raw in self.page.context.cookies()
        ]

    def set_cookies(self, cookies: Sequence[Cookie]) -> None:
        if not self.page:
            return

        raw_cookies: list[dict[str, Any]] = []
        for cookie in cookies:
            raw: dict[str, Any] = {
                "name": cookie.name,
                "value": cookie.value,
            }
            if cookie.domain:
                raw["domain"] = cookie.domain
                raw["path"] = cookie.path
            else:
                # Playwright requires either (domain + path) or url.
                raw["url"] = self.page.url
            if cookie.expires is not None:
                raw["expires"] = cookie.expires
            if cookie.http_only:
                raw["httpOnly"] = cookie.http_only
            if cookie.secure:
                raw["secure"] = cookie.secure
            if cookie.same_site:
                raw["sameSite"] = cookie.same_site
            raw_cookies.append(raw)

        self.page.context.add_cookies(raw_cookies)

    def get_headers(self) -> dict[str, str]:
        headers = dict(self._headers)
        if self.page:
            # The only header Playwright will actually let us read back
            # from a live page — everything else is write-only via
            # set_extra_http_headers(), so we fall back to what we
            # ourselves tracked for that.
            headers.setdefault(
                "User-Agent",
                self.page.evaluate("() => navigator.userAgent"),
            )
        return headers

    def set_headers(self, headers: dict[str, str]) -> None:
        self._headers.update(headers)
        if self.page:
            self.page.context.set_extra_http_headers(self._headers)
