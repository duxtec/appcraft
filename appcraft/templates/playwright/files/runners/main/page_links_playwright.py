from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.playwright.adapter import PlaywrightAdapter
from runners.main.page_links import PageLinksRunnerBase


class Playwright(PageLinksRunnerBase[PlaywrightAdapter], Runner):
    pass
