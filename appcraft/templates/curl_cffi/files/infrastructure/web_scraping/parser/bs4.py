from bs4 import BeautifulSoup
from bs4.element import Tag

from domain.html_elements.interface import HTMLReadingElementInterface
from infrastructure.web_scraping.parser.interface import HTMLParserInterface


class BeautifulSoupHTMLElement(HTMLReadingElementInterface):
    def __init__(self, element: Tag) -> None:
        self._element = element

    @property
    def inner_html(self) -> str:
        return str(self._element)

    @property
    def inner_text(self) -> str:
        return self._element.get_text()

    def has_attribute(self, name: str) -> bool:
        return self._element.has_attr(name)

    def get_attribute(self, name: str) -> str | None:
        attr = self._element.get(name)
        if isinstance(attr, list):
            return " ".join(attr)
        return attr


class BeautifulSoupParser(HTMLParserInterface):
    def parse(self, text: str) -> BeautifulSoup:
        return BeautifulSoup(text, features="html.parser")

    def select_one(
        self, tree: BeautifulSoup, selector: str
    ) -> BeautifulSoupHTMLElement | None:
        element = tree.select_one(selector)
        if element is None:
            return None
        return BeautifulSoupHTMLElement(element)

    def select_all(
        self, tree: BeautifulSoup, selector: str
    ) -> list[BeautifulSoupHTMLElement]:
        return [BeautifulSoupHTMLElement(el) for el in tree.select(selector)]
