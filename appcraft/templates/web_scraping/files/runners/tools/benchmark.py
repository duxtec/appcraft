from application.use_cases.web_scraping.benchmark import (
    BenchmarkInput,
    BenchmarkWebScrapingRunnersUseCase,
)
from infrastructure.framework.appcraft.core.runner import Runner
from presentation.cli.web_scraping.benchmark import BenchmarkCLIPresentation

# A deliberately huge, static, single-page document (several MB, thousands
# of nested elements) — a common stress-test page for HTML parsers, used
# here to separate real parser/engine speed differences from the network
# latency that dominates on a tiny page like example.com.
_HEAVY_PAGE_URL = "https://html.spec.whatwg.org/"
_HEAVY_PAGE_RUNS = 5


class WebScrapingBenchmark(Runner):
    @Runner.runner
    def run(self, *args: str, **kwargs: str):
        self._run_benchmark(kwargs)

    @Runner.runner
    def run_heavy_page(self, *args: str, **kwargs: str):
        """Same benchmark, pointed at a large page by default (override
        with urls=...) and with more repetitions — for comparing parser/
        engine speed on real parsing work, not just connection overhead.
        """
        kwargs.setdefault("urls", _HEAVY_PAGE_URL)
        kwargs.setdefault("runs", str(_HEAVY_PAGE_RUNS))
        self._run_benchmark(kwargs)

    def _run_benchmark(self, kwargs: dict[str, str]) -> None:
        benchmark_input = BenchmarkInput()
        if "runs" in kwargs:
            benchmark_input.runs = int(kwargs["runs"])
        if "urls" in kwargs:
            benchmark_input.urls = kwargs["urls"]

        use_case = BenchmarkWebScrapingRunnersUseCase()
        results = use_case.execute(benchmark_input)
        BenchmarkCLIPresentation.show_results(results)
