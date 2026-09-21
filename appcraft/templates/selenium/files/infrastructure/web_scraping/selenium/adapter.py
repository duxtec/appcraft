from typing import Any, Sequence, cast

from browser_manager.bases.browser_selenium import BrowserSelenium
from browser_manager.manager.selenium import BrowserManager
from domain.exceptions.web_scraping import NoBrowsersInstalledException
from domain.web_scraping.cookie import Cookie
from infrastructure.web_scraping.adapter import WebScrapingAdapterBase
from infrastructure.web_scraping.selenium.html_element import (
    SeleniumHTMLElement,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumAdapter(WebScrapingAdapterBase[SeleniumHTMLElement]):

    def __init__(self):
        self.browser_manager = BrowserManager()
        self.BROWSERS = self.browser_manager.BROWSERS

        self._browser: BrowserSelenium | None = None
        # Standard WebDriver has no cross-browser API to read or inject
        # arbitrary request headers — tracked here so get_headers()/
        # set_headers() have something consistent to return regardless
        # of browser, and actually applied via CDP where available
        # (Chrome-family only; see set_headers()).
        self._headers: dict[str, str] = {}
        super().__init__()

    @property
    def browser(self) -> BrowserSelenium:
        if self._browser:
            return self._browser

        # browser_manager's own enum/generic typing doesn't narrow
        # BROWSERS.CHROME.value down to BrowserSelenium specifically.
        default_browser = cast(BrowserSelenium, self.BROWSERS.CHROME.value())
        if default_browser.is_installed:
            # is_installed is an instance property — checking it on the
            # class itself (BROWSERS.CHROME.value.is_installed, without
            # instantiating first) returns the property object, which is
            # always truthy, so Chrome always "won" even when it isn't
            # actually installed.
            self._browser = default_browser
            return default_browser

        browsers = self.browser_manager.get_installeds()
        if not browsers:
            raise NoBrowsersInstalledException()
        self._browser = browsers[0]()
        return self._browser

    @browser.setter
    def browser(self, browser: type[BrowserSelenium]):
        self._browser = browser()

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

        if self.headless:
            options = self.browser.options
            options.add_argument("--headless")  # type: ignore

            if isinstance(self.browser, self.BROWSERS.CHROME.value):
                options.add_argument("--disable-gpu")  # type: ignore
                options.add_argument("--window-size=1920,1080")  # type: ignore
                options.add_argument("--no-sandbox")  # type: ignore
                options.add_argument("--disable-dev-shm-usage")  # type: ignore

    def start(self, *args: Any, **kwargs: Any):
        super().start(*args, **kwargs)
        self.driver = self.browser.driver

        self.wait = WebDriverWait(self.driver, self.timeout)

    def finish(self):
        self.driver.close()

    def open_page(self, url: str):
        self.driver.get(url)

    def query_selector(self, selector: str) -> SeleniumHTMLElement:
        element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return SeleniumHTMLElement(element, timeout=self.timeout)

    def query_selector_all(self, selector: str) -> list[SeleniumHTMLElement]:
        elements_self: list[SeleniumHTMLElement] = []
        elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        for element in elements:
            elements_self.append(SeleniumHTMLElement(element))
        return elements_self

    def get_cookies(self) -> list[Cookie]:
        return [
            Cookie(
                name=raw["name"],
                value=raw["value"],
                domain=raw.get("domain"),
                path=raw.get("path", "/"),
                secure=raw.get("secure", False),
                http_only=raw.get("httpOnly", False),
                expires=raw.get("expiry"),
                same_site=raw.get("sameSite"),
            )
            for raw in self.driver.get_cookies()
        ]

    def set_cookies(self, cookies: Sequence[Cookie]) -> None:
        # WebDriver only accepts cookies for the domain of the page
        # currently loaded — open_page() the target site before calling
        # this, or the browser will reject the cookie.
        for cookie in cookies:
            raw: dict[str, Any] = {"name": cookie.name, "value": cookie.value}
            if cookie.domain:
                raw["domain"] = cookie.domain
            if cookie.path:
                raw["path"] = cookie.path
            if cookie.secure:
                raw["secure"] = cookie.secure
            if cookie.expires:
                raw["expiry"] = int(cookie.expires)
            self.driver.add_cookie(raw)

    def get_headers(self) -> dict[str, str]:
        headers = dict(self._headers)
        # The one header every browser will actually tell us, cross-
        # browser and without CDP — everything else we only know if we
        # set it ourselves.
        headers.setdefault(
            "User-Agent",
            self.driver.execute_script("return navigator.userAgent"),
        )
        return headers

    def set_headers(self, headers: dict[str, str]) -> None:
        self._headers.update(headers)

        # Network.setExtraHTTPHeaders is Chrome DevTools Protocol, not
        # standard WebDriver — Firefox/geckodriver has no equivalent, so
        # this only actually reaches the browser on Chrome-family
        # drivers. get_headers() still reflects what was requested
        # either way, for handing off to another adapter.
        execute_cdp_cmd = getattr(self.driver, "execute_cdp_cmd", None)
        if callable(execute_cdp_cmd):
            execute_cdp_cmd(
                "Network.setExtraHTTPHeaders", {"headers": self._headers}
            )
