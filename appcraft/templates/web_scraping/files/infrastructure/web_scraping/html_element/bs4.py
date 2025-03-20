from bs4.element import Tag

from domain.interfaces.html_element.html_element import IHTMLReadingElement


class BeautifulSoupHTMLElement(IHTMLReadingElement):
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
