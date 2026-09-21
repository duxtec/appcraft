from ..template_abc import TemplateABC


class SeleniumTemplate(TemplateABC):
    active = True
    dependencies = ["web_scraping"]
    description = (
        "Selenium Template implements the Web Scraping Template's "
        "WebScrapingPort on top of Selenium WebDriver, for full browser "
        "automation (JS execution, clicks, form input). Combinable with "
        "the other web_scraping adapters (playwright, httpx, curl_cffi) "
        "— install whichever engines a given project needs, side by side."
    )
