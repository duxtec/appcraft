import importlib
from typing import Any

from application.ports.web_scraping import WebScrapingAsyncPort, WebScrapingPort
from domain.html_elements.interface import (
    HTMLInteractiveElementInterface,
    HTMLReadingElementInterface,
)
from infrastructure.framework.appcraft.core.config import Config

TInteractiveAdapter = (
    WebScrapingPort[HTMLInteractiveElementInterface]
    | WebScrapingAsyncPort[HTMLInteractiveElementInterface]
)
TReadingAdapter = (
    WebScrapingPort[HTMLReadingElementInterface]
    | WebScrapingAsyncPort[HTMLReadingElementInterface]
)

# Browser-automation engines — each can also stand in as the reading
# default, since HTMLInteractiveElementInterface is itself a
# HTMLReadingElementInterface.
_INTERACTIVE_BACKENDS: dict[str, tuple[str, str, str, str]] = {
    "playwright": (
        "infrastructure.framework.appcraft.templates.playwright",
        "PlaywrightTemplate",
        "infrastructure.web_scraping.playwright.adapter",
        "PlaywrightAdapter",
    ),
    "selenium": (
        "infrastructure.framework.appcraft.templates.selenium",
        "SeleniumTemplate",
        "infrastructure.web_scraping.selenium.adapter",
        "SeleniumAdapter",
    ),
}

# Plain-HTTP engines — fast, but read-only (no browser, so no
# HTMLInteractiveElementInterface).
_READING_BACKENDS: dict[str, tuple[str, str, str, str]] = {
    "httpx": (
        "infrastructure.framework.appcraft.templates.httpx",
        "HTTPXTemplate",
        "infrastructure.web_scraping.httpx.adapter",
        "HTTPXBeautifulSoupAdapter",
    ),
    "curl_cffi": (
        "infrastructure.framework.appcraft.templates.curl_cffi",
        "CurlCffiTemplate",
        "infrastructure.web_scraping.curl_cffi.adapter",
        "CurlCffiBeautifulSoupAdapter",
    ),
}

_default_interactive_adapter: TInteractiveAdapter | None = None
_default_reading_adapter: TReadingAdapter | None = None


def _load_backend(backend: tuple[str, str, str, str]) -> Any | None:
    template_module_name, template_class_name, adapter_module_name, adapter_class_name = (
        backend
    )
    try:
        template_module = importlib.import_module(template_module_name)
        template_class = getattr(template_module, template_class_name)

        if not template_class.is_installed():
            return None

        adapter_module = importlib.import_module(adapter_module_name)
        adapter_class = getattr(adapter_module, adapter_class_name)
        return adapter_class()
    except Exception:
        return None


def _load_first_installed(
    backends: dict[str, tuple[str, str, str, str]], configured: Any
) -> Any | None:
    names = list(backends)
    if configured in backends:
        names = [configured] + [name for name in names if name != configured]

    for name in names:
        adapter = _load_backend(backends[name])
        if adapter is not None:
            return adapter

    return None


def get_default_interactive_adapter() -> TInteractiveAdapter | None:
    """The default browser-automation adapter (playwright/selenium,
    config/web_scraping.toml's default_interactive_adapter picks which
    one first) — None if neither is installed.
    """
    global _default_interactive_adapter
    if _default_interactive_adapter is None:
        configured = Config().get("web_scraping").get(
            "default_interactive_adapter"
        )
        _default_interactive_adapter = _load_first_installed(
            _INTERACTIVE_BACKENDS, configured
        )
    return _default_interactive_adapter


def get_default_reading_adapter() -> TReadingAdapter | None:
    """The default read-only adapter — a fast HTTP-based one
    (httpx/curl_cffi) if installed; otherwise whichever interactive
    adapter is available, since a browser can do everything a
    read-only adapter can. None if nothing at all is installed.
    """
    global _default_reading_adapter
    if _default_reading_adapter is None:
        configured = Config().get("web_scraping").get(
            "default_reading_adapter"
        )
        _default_reading_adapter = _load_first_installed(
            _READING_BACKENDS, configured
        ) or get_default_interactive_adapter()
    return _default_reading_adapter


async def delegate_to_reading_adapter(
    interactive: TInteractiveAdapter,
) -> TReadingAdapter:
    """Call once the interactive-only part of a flow is done (login,
    solving a JS challenge, etc.): returns the default reading adapter
    with `interactive`'s session (cookies + headers) already copied
    over — or `interactive` itself, unchanged, if no faster adapter is
    installed (same session already, nothing to copy).

    Closes `interactive` when handing off to a genuinely different
    adapter, since its part of the flow is meant to be over at that
    point — call get_default_interactive_adapter() again for a fresh
    one if a later step needs the browser back.
    """
    reading = get_default_reading_adapter()

    if reading is None or reading is interactive:
        return interactive

    if isinstance(interactive, WebScrapingAsyncPort):
        session = await interactive.get_session()
    else:
        session = interactive.get_session()

    if isinstance(reading, WebScrapingAsyncPort):
        await reading.set_session(session)
    else:
        reading.set_session(session)

    if isinstance(interactive, WebScrapingAsyncPort):
        await interactive.finish()
    else:
        interactive.finish()

    # If `interactive` was the cached default, it's now closed —
    # don't hand out a dead adapter on the next
    # get_default_interactive_adapter() call.
    global _default_interactive_adapter
    if interactive is _default_interactive_adapter:
        _default_interactive_adapter = None

    return reading
