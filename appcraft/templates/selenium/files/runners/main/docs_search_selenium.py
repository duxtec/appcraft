from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.selenium.adapter import SeleniumAdapter
from runners.main.docs_search import DocsSearchRunnerBase


class Selenium(Runner, DocsSearchRunnerBase[SeleniumAdapter]):
    pass
