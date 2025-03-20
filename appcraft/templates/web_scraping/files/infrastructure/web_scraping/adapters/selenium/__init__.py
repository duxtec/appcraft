from typing import Any

from browser_manager.bases.browser_selenium import BrowserSelenium
from browser_manager.manager.selenium import BrowserManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from domain.exceptions.web_scraping import NoBrowsersInstalledException
from infrastructure.web_scraping.adapters.base import WebScrapingAdapterBase
from infrastructure.web_scraping.html_elements.selenium import (
    SeleniumHTMLElement,
)


class SeleniumAdapter(WebScrapingAdapterBase[SeleniumHTMLElement]):

    def __init__(self):
        self.browser_manager = BrowserManager()
        self.BROWSERS = self.browser_manager.BROWSERS

        self._browser: BrowserSelenium | None = None
        super().__init__()

    @property
    def browser(self) -> BrowserSelenium:
        if self._browser:
            return self._browser

        default_browser = self.BROWSERS.CHROME.value
        if default_browser.is_installed:
            self._browser = default_browser()
            return self._browser

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

            if isinstance(self.browser.__class__, self.BROWSERS.CHROME.value):
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
