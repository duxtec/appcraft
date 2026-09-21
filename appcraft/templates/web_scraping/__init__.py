from ..template_abc import TemplateABC


class WebScrapingTemplate(TemplateABC):
    active = True
    standalone = False
    description = (
        "Web Scraping Template is the foundational setup for extracting "
        "data from websites — the WebScrapingPort/WebScrapingAsyncPort "
        "contract, the HTMLElementInterface hierarchy parsed pages are "
        "exposed through, and the generic search/page-links example use "
        "cases and runners built on top of them. It ships no scraping "
        "engine of its own: install one or more of the selenium, "
        "playwright, httpx or curl_cffi templates (each depends on this "
        "one) to get an actual WebScrapingPort implementation. Those are "
        "freely combinable, not exclusive — a project can use httpx for "
        "static pages and playwright for JS-heavy ones side by side."
    )
