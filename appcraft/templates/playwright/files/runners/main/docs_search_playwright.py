from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.playwright.adapter import PlaywrightAdapter
from runners.main.docs_search import DocsSearchRunnerBase


class Playwright(Runner, DocsSearchRunnerBase[PlaywrightAdapter]):
    pass
