from application.ports.web_scraping import WebScrapingPort
from application.use_cases import UseCase
from domain.html_elements.interface import HTMLInteractiveElementInterface
from infrastructure.web_scraping.utils.keys import Keys


class SearchDocsUseCase(UseCase[str, list[HTMLInteractiveElementInterface]]):
    def __init__(
        self, adapter: WebScrapingPort[HTMLInteractiveElementInterface]
    ):
        self.adapter = adapter
        self._docs_url = "https://duxtec.github.io/appcraft/latest/"

    @property
    def docs_url(self):
        return self._docs_url

    @docs_url.setter
    def docs_url(self, value: str):
        self._docs_url = value

    def execute(
        self, input_data: str
    ) -> list[HTMLInteractiveElementInterface]:
        self.adapter.open_page(self.docs_url)
        search_input = self.adapter.query_selector(
            "#rtd-search-form > input[type=text]:nth-child(1)"
        )

        search_input.send_keys(input_data, Keys.ENTER)

        return self.adapter.query_selector_all("#search-results > ul > li")
