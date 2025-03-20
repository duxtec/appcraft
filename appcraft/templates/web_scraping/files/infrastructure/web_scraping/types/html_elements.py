from typing import TypeVar

from domain.interfaces.html_element.html_element import (
    IHTMLElement,
    IHTMLInteractiveElement,
    IHTMLNavigationElement,
    IHTMLReadingElement,
)

THTMLElement = TypeVar("THTMLElement", bound=IHTMLElement, covariant=True)
THTMLReadingElement = TypeVar(
    "THTMLReadingElement", bound=IHTMLReadingElement, covariant=True
)
THTMLNavigationElement = TypeVar(
    "THTMLNavigationElement", bound=IHTMLNavigationElement, covariant=True
)
THTMLInteractiveElement = TypeVar(
    "THTMLInteractiveElement", bound=IHTMLInteractiveElement, covariant=True
)
