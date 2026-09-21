from application.use_cases.web_scraping.docs import SearchDocsUseCase
from domain.html_elements.interface import HTMLInteractiveElementInterface
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class DocsSearchCLIPresentation:

    class Printer(ComponentPrinter):
        domain = "docs_search"

        @classmethod
        def starting(cls):
            cls.title("Starting scrapping")

        @classmethod
        def search_results(
            cls, results: list[HTMLInteractiveElementInterface]
        ):
            for result in results:
                title = result.query_selector("a")
                link = title.get_attribute("href")
                content = result.query_selector("p")

                cls.title(title.inner_text)
                if link:
                    cls.info(link)

                print(content.inner_text)
                print("\n\n")

    def __init__(self, search_docs_uc: SearchDocsUseCase) -> None:
        self.search_docs_uc = search_docs_uc

    def search(self, query: str) -> None:
        results = self.search_docs_uc.execute(query)
        self.Printer.search_results(results)

    def start(self) -> None:
        self.Printer.starting()
