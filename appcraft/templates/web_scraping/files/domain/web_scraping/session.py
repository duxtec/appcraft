from dataclasses import dataclass, field

from domain.web_scraping.cookie import Cookie


@dataclass(frozen=True)
class WebScrapingSession:
    """A full session snapshot — cookies + headers together — so a
    session started in one adapter can continue in another with a
    single get_session()/set_session() call instead of copying cookies
    and headers separately:
    `httpx_adapter.set_session(selenium_adapter.get_session())`.
    """

    cookies: list[Cookie] = field(default_factory=list)
    headers: dict[str, str] = field(default_factory=dict)
