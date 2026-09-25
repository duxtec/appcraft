import asyncio
from abc import ABC, abstractmethod
from typing import Any, Generic

from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingSyncOrAsyncAdapter,
)


class WebScrapingRunnerBase(ABC, Generic[TWebScrapingSyncOrAsyncAdapter]):
    """Shared by the concrete runners in runners/main/ (docs_search.py,
    page_links.py): parses the --headless CLI flag and dispatches
    adapter.start() correctly whether the resolved adapter is sync or
    async. Each concrete runner provides its own `adapter` property
    (resolving whichever engine is installed/configured as the
    default) — this base doesn't derive one automatically.
    """

    _adapter: TWebScrapingSyncOrAsyncAdapter | None = None

    @property
    @abstractmethod
    def adapter(self) -> TWebScrapingSyncOrAsyncAdapter: ...

    def start(self, *args: str, **kwargs: str):
        headless = "--headless" in args
        adapter_args = tuple(
            arg for arg in args if arg != "--headless"
        )
        adapter_kwargs: dict[str, Any] = kwargs
        adapter_kwargs.setdefault("headless", headless)

        if isinstance(self.adapter, WebScrapingAsyncAdapterBase):
            asyncio.run(self.adapter.start(*adapter_args, **adapter_kwargs))
        else:
            self.adapter.start(*adapter_args, **adapter_kwargs)
