from ..template_abc import TemplateABC


class HTTPXTemplate(TemplateABC):
    active = True
    dependencies = ["web_scraping"]
    description = (
        "HTTPX Template implements the Web Scraping Template's "
        "WebScrapingAsyncPort on top of httpx (async HTTP client) "
        "paired with BeautifulSoup or selectolax for parsing — fast, "
        "no browser, for pages that don't need JS execution. Combinable "
        "with the other web_scraping adapters (selenium, playwright, "
        "curl_cffi) — install whichever engines a given project needs, "
        "side by side."
    )
