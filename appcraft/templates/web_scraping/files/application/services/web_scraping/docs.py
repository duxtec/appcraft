from domain.interfaces.html_element.html_element import (
    IHTMLInteractiveElement,
)
from infrastructure.web_scraping.interfaces.adapters import (
    WebScrapingAdapterInterface,
)
from infrastructure.web_scraping.utils.keys import Keys


class DocScrapService:
    def __init__(
        self, adapter: WebScrapingAdapterInterface[IHTMLInteractiveElement]
    ):
        self.adapter = adapter
        self._docs_url = "https://duxtec.github.io/appcraft/latest/"

    @property
    def docs_url(self):
        return self._docs_url

    @docs_url.setter
    def docs_url(self, value: str):
        self._docs_url = value

    def search(self, value: str) -> list[IHTMLInteractiveElement]:
        self.adapter.open_page(self.docs_url)
        search_input = self.adapter.query_selector(
            "#rtd-search-form > input[type=text]:nth-child(1)"
        )

        search_input.send_keys(value, Keys.ENTER)

        results = self.adapter.query_selector_all("#search-results > ul > li")

        return results
