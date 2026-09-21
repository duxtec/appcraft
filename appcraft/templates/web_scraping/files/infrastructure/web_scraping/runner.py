import asyncio
from abc import ABC
from typing import Any, Generic

from infrastructure.framework.appcraft.core.property_meta import PropertyMeta
from infrastructure.web_scraping.adapter import WebScrapingAsyncAdapterBase
from infrastructure.web_scraping.types.adapters import (
    TWebScrapingAdapterInteractive,
    TWebScrapingAdapterNavigation,
    TWebScrapingAdapterReading,
    TWebScrapingSyncOrAsyncAdapter,
)


class WebScrapingRunnerBase(
    ABC,
    Generic[TWebScrapingSyncOrAsyncAdapter],
    metaclass=PropertyMeta,
):
    """Generic runner mixin — subscript with a concrete adapter class to
    get a runnable Runner subclass, e.g.:
    `class Selenium(Runner, DocsSearchRunnerBase[SeleniumAdapter]): pass`
    PropertyMeta reads that subscript (via __orig_bases__) and sets
    `_adapter_cls` automatically — no method needs overriding.

    Lives in infrastructure/, not runners/, so application/ (e.g. the
    benchmark use case, which filters discovered runners by
    `issubclass(app, WebScrapingRunnerBase)`) can depend on it without
    reaching into the runners layer.
    """

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


class WebScrapingReaderRunnerBase(
    WebScrapingRunnerBase[TWebScrapingAdapterReading],
    ABC,
    Generic[TWebScrapingAdapterReading],
):
    pass


class WebScrapingNavigationRunnerBase(
    WebScrapingRunnerBase[TWebScrapingAdapterNavigation],
    ABC,
    Generic[TWebScrapingAdapterNavigation],
):
    pass


class WebScrapingInteractiveRunnerBase(
    WebScrapingRunnerBase[TWebScrapingAdapterInteractive],
    ABC,
):
    pass
