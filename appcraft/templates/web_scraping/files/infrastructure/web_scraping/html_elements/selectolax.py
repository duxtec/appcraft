from selectolax.parser import Node

from domain.interfaces.html_element.html_element import IHTMLReadingElement


class SelectolaxHTMLElement(IHTMLReadingElement):
    def __init__(
        self,
        element: Node,
    ) -> None:
        self._element = element

    @property
    def inner_html(self) -> str:
        html = self._element.html or ""
        return html

    @property
    def inner_text(self) -> str:
        text = self._element.text()
        return text

    def has_attribute(self, name: str) -> bool:
        if self._element.attributes.get(name) is None:
            return False
        return True

    def get_attribute(self, name: str) -> str | None:
        return self._element.attributes.get(name)
