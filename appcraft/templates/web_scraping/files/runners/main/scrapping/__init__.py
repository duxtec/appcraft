import asyncio
from abc import ABC
from typing import Any, Generic

from infrastructure.framework.appcraft.core.property_meta import PropertyMeta
from infrastructure.web_scraping.adapters.base import (
    WebScrapingAsyncAdapterBase,
)
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingAdapterInteractive,
    TWebScrapingAdapterNavigation,
    TWebScrapingAdapterReading,
    TWebScrapingSyncOrAsyncAdapter,
)


class RunnerScrap(
    ABC,
    Generic[TWebScrapingSyncOrAsyncAdapter],
    metaclass=PropertyMeta,
):
    _props = ["_adapter_cls"]
    _adapter_cls: type[TWebScrapingSyncOrAsyncAdapter]
    _adapter: TWebScrapingSyncOrAsyncAdapter | None = None

    def start(self, *args: str, **kwargs: str):
        headless = "--headless" in args
        adapter_args = args
        adapter_kwargs: dict[str, Any] = kwargs

        adapter_args = tuple(
            arg for arg in adapter_args if arg != "--headless"
        )
        adapter_kwargs.setdefault("headless", headless)

        if isinstance(self.adapter, WebScrapingAsyncAdapterBase):
            asyncio.run(self.adapter.start(*adapter_args, **adapter_kwargs))
        else:
            self.adapter.start(*adapter_args, **adapter_kwargs)

    @property
    def adapter(
        self,
    ) -> TWebScrapingSyncOrAsyncAdapter:
        if not self._adapter:
            self._adapter = self._adapter_cls()
        return self._adapter


class RunnerReaderScrap(
    RunnerScrap[TWebScrapingAdapterReading],
    ABC,
    Generic[TWebScrapingAdapterReading],
):
    pass


class RunnerNavigationScrap(
    RunnerScrap[TWebScrapingAdapterNavigation],
    ABC,
    Generic[TWebScrapingAdapterNavigation],
):
    pass


class RunnerInteractiveScrap(
    RunnerScrap[TWebScrapingAdapterInteractive],
    ABC,
):
    pass
