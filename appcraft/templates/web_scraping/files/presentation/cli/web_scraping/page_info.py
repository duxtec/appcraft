import re
from typing import Sequence

from application.use_cases.web_scraping.page_info import (
    GetPageLinksUseCase,
    TLink,
)
from domain.html_elements.interface import HTMLReadingElementInterface
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class PageLinksCLIPresentation(ComponentPrinter):
    domain = "page_links"

    def __init__(self, get_page_links_uc: GetPageLinksUseCase) -> None:
        self.get_page_links_uc = get_page_links_uc

    def show_links(self, urls: list[str] | None = None) -> None:
        links = self.get_page_links_uc.execute(urls)
        self._print_links(links)

    @classmethod
    def _print_links(cls, links: Sequence[TLink]):
        for link in links:
            if isinstance(link, HTMLReadingElementInterface):
                name = link.inner_text
                href = link.get_attribute("href")
            else:
                name = link.get("Name") or ""
                href = link.get("Href")

            name = re.sub(r"\s+", " ", name).strip()

            cls.title("Name", end=f": {name}\n")
            cls.title("Href", end=f": {href}\n\n")
