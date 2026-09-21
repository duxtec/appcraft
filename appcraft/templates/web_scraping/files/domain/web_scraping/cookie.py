from dataclasses import dataclass


@dataclass(frozen=True)
class Cookie:
    """Engine-agnostic cookie — what WebScrapingPort.get_cookies()/
    set_cookies() exchange. Each adapter translates to/from its own
    library's native cookie shape, so a session can start in one engine
    (e.g. Selenium, to get past a login/JS challenge) and continue in
    another (e.g. httpx, for fast bulk requests) by carrying these
    across: `httpx_adapter.set_cookies(selenium_adapter.get_cookies())`.
    """

    name: str
    value: str
    domain: str | None = None
    path: str = "/"
    secure: bool = False
    http_only: bool = False
    expires: float | None = None
    same_site: str | None = None
