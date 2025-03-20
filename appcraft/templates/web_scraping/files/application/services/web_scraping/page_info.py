import asyncio

from domain.interfaces.html_element.html_element import IHTMLReadingElement
from infrastructure.web_scraping.interfaces.adapters import (
    WebScrapingAdapterInterface,
    WebScrapingAsyncAdapterInterface,
)


class PageInfoScrapService:
    def __init__(
        self,
        adapter: (
            WebScrapingAdapterInterface[IHTMLReadingElement]
            | WebScrapingAsyncAdapterInterface[IHTMLReadingElement]
        ),
    ):
        self.adapter = adapter

    def get_links(
        self, urls: list[str] | None = None
    ) -> list[IHTMLReadingElement | dict[str, str]]:
        links: list[IHTMLReadingElement | dict[str, str]] = []
        if not urls:
            urls = [
                "https://duxtec.github.io/appcraft/latest/",
                "https://github.com/duxtec/appcraft",
            ]

        if isinstance(self.adapter, WebScrapingAsyncAdapterInterface):
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

    async def _async_get_links(
        self, urls: list[str]
    ) -> list[IHTMLReadingElement | dict[str, str]]:
        async def get_links(url: str) -> list[IHTMLReadingElement]:
            links = []
            if isinstance(self.adapter, WebScrapingAsyncAdapterInterface):
                await self.adapter.open_page(url)
                links = await self.adapter.query_selector_all("a")

            return links

        if isinstance(self.adapter, WebScrapingAsyncAdapterInterface):
            tasks = [get_links(url) for url in urls]
            results = await asyncio.gather(*tasks)
            links: list[IHTMLReadingElement | dict[str, str]] = []
            for result in results:
                links += result
            return links
        return []
