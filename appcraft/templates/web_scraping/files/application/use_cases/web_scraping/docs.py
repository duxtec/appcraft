import asyncio

from application.ports.web_scraping import (
    WebScrapingAsyncPort,
    WebScrapingPort,
)
from application.use_cases import UseCase
from domain.html_elements.interface import HTMLInteractiveElementInterface
from domain.web_scraping.keys import Keys

TAdapter = (
    WebScrapingPort[HTMLInteractiveElementInterface]
    | WebScrapingAsyncPort[HTMLInteractiveElementInterface]
)


class SearchDocsUseCase(UseCase[str, list[HTMLInteractiveElementInterface]]):
    def __init__(self, adapter: TAdapter):
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
        if isinstance(self.adapter, WebScrapingAsyncPort):
            return asyncio.run(self._execute_async(input_data))

        self.adapter.open_page(self.docs_url)
        search_input = self.adapter.query_selector(
            "#rtd-search-form > input[type=text]:nth-child(1)"
        )
        search_input.send_keys(input_data, Keys.ENTER)

        return self.adapter.query_selector_all("#search-results > ul > li")

    async def _execute_async(
        self, input_data: str
    ) -> list[HTMLInteractiveElementInterface]:
        assert isinstance(self.adapter, WebScrapingAsyncPort)

        await self.adapter.open_page(self.docs_url)
        search_input = await self.adapter.query_selector(
            "#rtd-search-form > input[type=text]:nth-child(1)"
        )
        # send_keys is a plain (non-async) method on the domain element
        # interface, regardless of which engine produced the element.
        search_input.send_keys(input_data, Keys.ENTER)

        return await self.adapter.query_selector_all(
            "#search-results > ul > li"
        )
