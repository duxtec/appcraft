from ..template_abc import TemplateABC


class CurlCffiTemplate(TemplateABC):
    active = True
    dependencies = ["web_scraping"]
    description = (
        "curl_cffi Template implements the Web Scraping Template's "
        "WebScrapingAsyncPort on top of curl_cffi (paired with "
        "BeautifulSoup or selectolax for parsing) — like httpx, no "
        "browser, but impersonates a real browser's TLS/JA3 fingerprint "
        "to get past anti-bot fingerprinting that a plain HTTP client "
        "would get blocked on. Combinable with the other web_scraping "
        "adapters (selenium, playwright, httpx) — install whichever "
        "engines a given project needs, side by side."
    )
