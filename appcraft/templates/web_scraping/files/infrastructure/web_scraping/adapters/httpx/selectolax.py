from selectolax.parser import HTMLParser

from infrastructure.web_scraping.adapters.httpx import HTTPXAdapter
from infrastructure.web_scraping.exceptions import NoSuchElementException
from infrastructure.web_scraping.html_elements.selectolax import (
    SelectolaxHTMLElement,
)


class HTTPXSelectolaxAdapter(HTTPXAdapter[SelectolaxHTMLElement]):
    def __init__(self):
        super().__init__()
        self.tree: HTMLParser | None = None

    async def html_parser(self, text: str):
        return HTMLParser(text)

    async def query_selector(self, selector: str):
        if self.tree:
            element = self.tree.css_first(selector)
            if element:
                return SelectolaxHTMLElement(element)
            raise NoSuchElementException()
        raise NoSuchElementException()

    async def query_selector_all(
        self, selector: str
    ) -> list[SelectolaxHTMLElement]:
        if self.tree:
            elements = self.tree.css(selector)
            return [SelectolaxHTMLElement(el) for el in elements]
        return []
