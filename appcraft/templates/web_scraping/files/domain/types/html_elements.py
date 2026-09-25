from typing import TypeVar

from domain.html_elements.interface import HTMLElementInterface

THTMLElement = TypeVar(
    "THTMLElement", bound=HTMLElementInterface, covariant=True
)
