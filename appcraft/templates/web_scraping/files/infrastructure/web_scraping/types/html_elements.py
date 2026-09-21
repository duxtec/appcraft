from typing import TypeVar

from domain.html_elements.interface import (
    HTMLElementInterface,
    HTMLInteractiveElementInterface,
    HTMLNavigationElementInterface,
    HTMLReadingElementInterface,
)

THTMLElement = TypeVar(
    "THTMLElement", bound=HTMLElementInterface, covariant=True
)
THTMLReadingElement = TypeVar(
    "THTMLReadingElement", bound=HTMLReadingElementInterface, covariant=True
)
THTMLNavigationElement = TypeVar(
    "THTMLNavigationElement",
    bound=HTMLNavigationElementInterface,
    covariant=True,
)
THTMLInteractiveElement = TypeVar(
    "THTMLInteractiveElement",
    bound=HTMLInteractiveElementInterface,
    covariant=True,
)
