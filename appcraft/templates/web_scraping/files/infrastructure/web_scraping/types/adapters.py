from typing import TypeVar

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from domain.html_elements.interface import (
    HTMLElementInterface,
    HTMLInteractiveElementInterface,
    HTMLNavigationElementInterface,
    HTMLReadingElementInterface,
)

TWebScrapingAdapter = TypeVar(
    "TWebScrapingAdapter",
    bound=WebScrapingPort[HTMLElementInterface],
    covariant=True,
)

TWebScrapingAdapterReading = TypeVar(
    "TWebScrapingAdapterReading",
    bound=WebScrapingPort[HTMLReadingElementInterface],
    covariant=True,
)

TWebScrapingAdapterNavigation = TypeVar(
    "TWebScrapingAdapterNavigation",
    bound=WebScrapingPort[HTMLNavigationElementInterface],
    covariant=True,
)

TWebScrapingAdapterInteractive = TypeVar(
    "TWebScrapingAdapterInteractive",
    bound=WebScrapingPort[HTMLInteractiveElementInterface],
    covariant=True,
)


TWebScrapingAsyncAdapter = TypeVar(
    "TWebScrapingAsyncAdapter",
    bound=WebScrapingAsyncPort[HTMLElementInterface],
    covariant=True,
)

TWebScrapingAsyncAdapterReading = TypeVar(
    "TWebScrapingAsyncAdapterReading",
    bound=WebScrapingAsyncPort[HTMLReadingElementInterface],
    covariant=True,
)

TWebScrapingAsyncAdapterNavigation = TypeVar(
    "TWebScrapingAsyncAdapterNavigation",
    bound=WebScrapingAsyncPort[HTMLNavigationElementInterface],
    covariant=True,
)

TWebScrapingAsyncAdapterInteractive = TypeVar(
    "TWebScrapingAsyncAdapterInteractive",
    bound=WebScrapingAsyncPort[HTMLInteractiveElementInterface],
    covariant=True,
)


TWebScrapingSyncOrAsyncAdapter = TypeVar(
    "TWebScrapingSyncOrAsyncAdapter",
    bound=WebScrapingPort[HTMLElementInterface]
    | WebScrapingAsyncPort[HTMLElementInterface],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterReading = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterReading",
    bound=WebScrapingPort[HTMLReadingElementInterface]
    | WebScrapingAsyncPort[HTMLReadingElementInterface],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterNavigation = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterNavigation",
    bound=WebScrapingPort[HTMLNavigationElementInterface]
    | WebScrapingAsyncPort[HTMLNavigationElementInterface],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterInteractive = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterInteractive",
    bound=WebScrapingPort[HTMLInteractiveElementInterface]
    | WebScrapingAsyncPort[HTMLInteractiveElementInterface],
    covariant=True,
)
