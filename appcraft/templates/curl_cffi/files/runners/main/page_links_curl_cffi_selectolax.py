from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.web_scraping.curl_cffi.adapter import (
    CurlCffiSelectolaxAdapter,
)
from runners.main.page_links import PageLinksRunnerBase


class CurlCffiSelectolax(
    PageLinksRunnerBase[CurlCffiSelectolaxAdapter], Runner
):
    pass
