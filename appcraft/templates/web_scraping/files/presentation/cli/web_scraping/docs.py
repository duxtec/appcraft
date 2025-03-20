from application.services.web_scraping.docs import DocScrapService
from domain.interfaces.html_element.html_element import (
    IHTMLInteractiveElement,
)
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class DocScrapPresenter:

    class Printer(ComponentPrinter):
        domain = "docscrap"

        @classmethod
        def starting(cls):
            cls.title("Starting scrapping")

        @classmethod
        def search_results(cls, results: list[IHTMLInteractiveElement]):
            for result in results:
                title = result.query_selector("a")
                link = title.get_attribute("href")
                content = result.query_selector("p")

                cls.title(title.inner_text)
                if link:
                    cls.info(link)

                print(content.inner_text)
                print("\n\n")

    def __init__(self, service: DocScrapService) -> None:
        self.service = service

    def show_search_results(
        self, results: list[IHTMLInteractiveElement]
    ) -> None:
        # results = self.service.search()
        self.Printer.search_results(results)

    def start(self) -> None:
        self.Printer.starting()
