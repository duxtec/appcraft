from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.selenium.adapter import SeleniumAdapter
from runners.main.page_links import PageLinksRunnerBase


class Selenium(PageLinksRunnerBase[SeleniumAdapter], Runner):
    pass
