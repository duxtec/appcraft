from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.curl_cffi.adapter import (
    CurlCffiBeautifulSoupAdapter,
)
from runners.main.page_links import PageLinksRunnerBase


class CurlCffiBeautifulSoup(
    PageLinksRunnerBase[CurlCffiBeautifulSoupAdapter], Runner
):
    pass
