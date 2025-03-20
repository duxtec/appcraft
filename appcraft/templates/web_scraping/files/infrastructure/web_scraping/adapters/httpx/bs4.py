from bs4 import BeautifulSoup

from infrastructure.web_scraping.adapters.httpx import HTTPXAdapter
from infrastructure.web_scraping.exceptions import NoSuchElementException
from infrastructure.web_scraping.html_elements.bs4 import (
    BeautifulSoupHTMLElement,
)


class HTTPXBeautifulSoupAdapter(HTTPXAdapter[BeautifulSoupHTMLElement]):
    def __init__(self):
        super().__init__()
        self.tree: BeautifulSoup | None = None

    async def html_parser(self, text: str):
        return BeautifulSoup(text)

    async def query_selector(self, selector: str):
        if self.tree:
            element = self.tree.select_one(selector)
            if element:
                return BeautifulSoupHTMLElement(element)
            raise NoSuchElementException()
        raise NoSuchElementException()

    async def query_selector_all(
        self, selector: str
    ) -> list[BeautifulSoupHTMLElement]:
        if self.tree:
            elements = self.tree.select(selector)
            return [BeautifulSoupHTMLElement(el) for el in elements]
        return []
