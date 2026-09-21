import subprocess
import sys

from infrastructure.framework.appcraft.utils.printer import Printer

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
        # separately from the pip package — this can only run after
        # "Installing requirements" put the playwright CLI on PATH.
        try:
            subprocess.check_call(["playwright", "install", "chromium"])
        except subprocess.CalledProcessError as e:
            Printer.error(str(e))
            sys.exit(1)
