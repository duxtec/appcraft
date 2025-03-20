import re

from application.services.web_scraping.page_info import PageInfoScrapService
from domain.interfaces.html_element.html_element import IHTMLReadingElement
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class PageInfoScrapPresenter(ComponentPrinter):
    domain = "pageinfo"

    @classmethod
    def starting(cls):
        cls.title("Starting scrapping")

    @classmethod
    def show_links(cls, links: list[IHTMLReadingElement | dict[str, str]]):
        for link in links:
            if isinstance(link, IHTMLReadingElement):
                name = link.inner_text
                href = link.get_attribute("href")
            else:
                name = link.get("Name", "")
                href = link.get("Href", "")

            name = re.sub(r"\s+", " ", name).strip()

            cls.title("Name", end=f": {name}\n")
            cls.title("Href", end=f": {href}\n\n")

    def __init__(self, service: PageInfoScrapService) -> None:
        self.service = service
