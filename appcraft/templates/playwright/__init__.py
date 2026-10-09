from infrastructure.core.package.manager import PackageManagerBase

from ..template_abc import TemplateABC


class PlaywrightTemplate(TemplateABC):
    active = True
    dependencies = ["web_scraping"]
    description = (
        "Playwright Template implements the Web Scraping Template's "
        "WebScrapingPort on top of Playwright, for full browser "
        "automation (JS execution, clicks, form input) across "
        "Chromium/Firefox/WebKit. Combinable with the other web_scraping "
        "adapters (selenium, httpx, curl_cffi) — install whichever "
        "engines a given project needs, side by side."
    )

    @classmethod
    def post_install(cls, target_dir: str | None = None) -> None:
        # Playwright needs its own browser binaries, downloaded
        # separately from the pip package. Not subprocess.check_call
        # directly: the "playwright" CLI script lives inside this
        # generated project's own (Poetry/Pipenv/uv) venv, which isn't
        # necessarily activated in — or even the same venv as —
        # whichever Python is running appcraft itself, so a bare
        # subprocess call can't find it. PackageManagerBase().run_command()
        # wraps it correctly per active manager (e.g. `poetry run
        # playwright ...`).
        PackageManagerBase().run_command(["playwright", "install", "chromium"])
