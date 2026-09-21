import asyncio

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from application.use_cases import UseCase
from domain.html_elements.interface import HTMLReadingElementInterface

TLink = HTMLReadingElementInterface | dict[str, str | None]


class GetPageLinksUseCase(UseCase[list[str] | None, list[TLink]]):
    def __init__(
        self,
        adapter: (
            WebScrapingPort[HTMLReadingElementInterface]
            | WebScrapingAsyncPort[HTMLReadingElementInterface]
        ),
    ):
        self.adapter = adapter

    def execute(self, input_data: list[str] | None = None) -> list[TLink]:
        urls = input_data
        links: list[TLink] = []
        if not urls:
            urls = [
                "https://duxtec.github.io/appcraft/latest/",
                "https://github.com/duxtec/appcraft",
            ]

        if isinstance(self.adapter, WebScrapingAsyncPort):
            links = asyncio.run(self._async_get_links(urls))
        else:
            for url in urls:
                self.adapter.open_page(url)
                page_links = self.adapter.query_selector_all("a")
                links += [
                    {
                        "Name": link.inner_text,
                        "Href": link.get_attribute("href"),
                    }
                    for link in page_links
                ]

        return links

    async def _async_get_links(self, urls: list[str]) -> list[TLink]:
        async def get_links(url: str) -> list[HTMLReadingElementInterface]:
            links = []
            if isinstance(self.adapter, WebScrapingAsyncPort):
                await self.adapter.open_page(url)
                links = await self.adapter.query_selector_all("a")

            return links

        if isinstance(self.adapter, WebScrapingAsyncPort):
            tasks = [get_links(url) for url in urls]
            results = await asyncio.gather(*tasks)
            links: list[TLink] = []
            for result in results:
                links += result
            return links
        return []
