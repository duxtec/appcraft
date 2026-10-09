from typing import TypeVar

from domain.html_elements.interface import HTMLElement

THTMLElement = TypeVar(
    "THTMLElement", bound=HTMLElement, covariant=True
)
