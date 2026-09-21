from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.httpx.adapter import HTTPXBeautifulSoupAdapter
from runners.main.page_links import PageLinksRunnerBase


class HTTPXBeautifulSoup(PageLinksRunnerBase[HTTPXBeautifulSoupAdapter], Runner):
    pass
