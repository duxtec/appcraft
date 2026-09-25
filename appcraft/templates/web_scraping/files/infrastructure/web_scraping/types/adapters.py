from typing import TypeVar

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from domain.html_elements.interface import HTMLElementInterface

TWebScrapingSyncOrAsyncAdapter = TypeVar(
    "TWebScrapingSyncOrAsyncAdapter",
    bound=WebScrapingPort[HTMLElementInterface]
    | WebScrapingAsyncPort[HTMLElementInterface],
    covariant=True,
)
