from application.use_cases.web_scraping.benchmark import BenchmarkResult
from infrastructure.framework.appcraft.utils.component_printer import (
    ComponentPrinter,
)


class BenchmarkCLIPresentation(ComponentPrinter):
    domain = "web_scraping_benchmark"

    @classmethod
    def show_results(cls, results: list[BenchmarkResult]) -> None:
        if not results:
            cls.warning(
                "No web scraping runners found — add selenium, "
                "playwright, httpx or curl_cffi first."
            )
            return

        succeeded = sorted(
            (result for result in results if result.error is None),
            key=lambda result: result.avg_seconds or float("inf"),
        )
        failed = [result for result in results if result.error is not None]

        cls.title("Web scraping runner benchmark (fastest first)")
        for result in succeeded:
            cls.success(result.name, end=": ")
            avg = result.avg_seconds or 0.0
            print(
                f"avg {avg:.3f}s "
                f"(min {min(result.elapsed_seconds):.3f}s, "
                f"max {max(result.elapsed_seconds):.3f}s, "
                f"{len(result.elapsed_seconds)} runs)"
            )

        for result in failed:
            cls.error(result.name, end=": ")
            print(result.error)
