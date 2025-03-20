from typing import TypeVar

from domain.interfaces.html_element.html_element import (
    IHTMLElement,
    IHTMLInteractiveElement,
    IHTMLNavigationElement,
    IHTMLReadingElement,
)
from infrastructure.web_scraping.interfaces.adapters import (
    WebScrapingAdapterInterface,
    WebScrapingAsyncAdapterInterface,
)

TWebScrapingAdapter = TypeVar(
    "TWebScrapingAdapter",
    bound=WebScrapingAdapterInterface[IHTMLElement],
    covariant=True,
)

TWebScrapingAdapterReading = TypeVar(
    "TWebScrapingAdapterReading",
    bound=WebScrapingAdapterInterface[IHTMLReadingElement],
    covariant=True,
)

TWebScrapingAdapterNavigation = TypeVar(
    "TWebScrapingAdapterNavigation",
    bound=WebScrapingAdapterInterface[IHTMLNavigationElement],
    covariant=True,
)

TWebScrapingAdapterInteractive = TypeVar(
    "TWebScrapingAdapterInteractive",
    bound=WebScrapingAdapterInterface[IHTMLInteractiveElement],
    covariant=True,
)


TWebScrapingAsyncAdapter = TypeVar(
    "TWebScrapingAsyncAdapter",
    bound=WebScrapingAsyncAdapterInterface[IHTMLElement],
    covariant=True,
)

TWebScrapingAsyncAdapterReading = TypeVar(
    "TWebScrapingAsyncAdapterReading",
    bound=WebScrapingAsyncAdapterInterface[IHTMLReadingElement],
    covariant=True,
)

TWebScrapingAsyncAdapterNavigation = TypeVar(
    "TWebScrapingAsyncAdapterNavigation",
    bound=WebScrapingAsyncAdapterInterface[IHTMLNavigationElement],
    covariant=True,
)

TWebScrapingAsyncAdapterInteractive = TypeVar(
    "TWebScrapingAsyncAdapterInteractive",
    bound=WebScrapingAsyncAdapterInterface[IHTMLInteractiveElement],
    covariant=True,
)


TWebScrapingSyncOrAsyncAdapter = TypeVar(
    "TWebScrapingSyncOrAsyncAdapter",
    bound=WebScrapingAdapterInterface[IHTMLElement]
    | WebScrapingAsyncAdapterInterface[IHTMLElement],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterReading = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterReading",
    bound=WebScrapingAdapterInterface[IHTMLReadingElement]
    | WebScrapingAsyncAdapterInterface[IHTMLReadingElement],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterNavigation = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterNavigation",
    bound=WebScrapingAdapterInterface[IHTMLNavigationElement]
    | WebScrapingAsyncAdapterInterface[IHTMLNavigationElement],
    covariant=True,
)

TWebScrapingSyncOrAsyncAdapterInteractive = TypeVar(
    "TWebScrapingSyncOrAsyncAdapterInteractive",
    bound=WebScrapingAdapterInterface[IHTMLInteractiveElement]
    | WebScrapingAsyncAdapterInterface[IHTMLInteractiveElement],
    covariant=True,
)
