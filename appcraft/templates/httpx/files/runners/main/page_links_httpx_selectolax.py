from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.httpx.adapter import HTTPXSelectolaxAdapter
from runners.main.page_links import PageLinksRunnerBase


class HTTPXSelectolax(PageLinksRunnerBase[HTTPXSelectolaxAdapter], Runner):
    pass
