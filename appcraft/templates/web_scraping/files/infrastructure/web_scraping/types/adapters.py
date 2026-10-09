from typing import TypeVar

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from domain.html_elements.interface import HTMLElement

TWebScrapingSyncOrAsyncAdapter = TypeVar(
    "TWebScrapingSyncOrAsyncAdapter",
    bound=WebScrapingPort[HTMLElement]
    | WebScrapingAsyncPort[HTMLElement],
    covariant=True,
)
