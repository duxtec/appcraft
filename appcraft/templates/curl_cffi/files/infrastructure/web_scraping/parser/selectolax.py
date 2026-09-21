from selectolax.parser import HTMLParser, Node

from domain.html_elements.interface import HTMLReadingElementInterface
from infrastructure.web_scraping.parser.interface import HTMLParserInterface


class SelectolaxHTMLElement(HTMLReadingElementInterface):
    def __init__(self, element: Node) -> None:
        self._element = element

    @property
    def inner_html(self) -> str:
        return self._element.html or ""

    @property
    def inner_text(self) -> str:
        return self._element.text()

    def has_attribute(self, name: str) -> bool:
        return self._element.attributes.get(name) is not None

    def get_attribute(self, name: str) -> str | None:
        return self._element.attributes.get(name)


class SelectolaxParser(HTMLParserInterface):
    def parse(self, text: str) -> HTMLParser:
        return HTMLParser(text)

    def select_one(
        self, tree: HTMLParser, selector: str
    ) -> SelectolaxHTMLElement | None:
        element = tree.css_first(selector)
        if element is None:
            return None
        return SelectolaxHTMLElement(element)

    def select_all(
        self, tree: HTMLParser, selector: str
    ) -> list[SelectolaxHTMLElement]:
        return [SelectolaxHTMLElement(el) for el in tree.css(selector)]
