import asyncio
import importlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from application.ports.web_scraping import WebScrapingAsyncPort
from application.use_cases import UseCase

# Every (engine, adapter, action) combination this benchmark knows how to
# time — checked against each engine template's own is_installed() so
# only what's actually installed gets benchmarked. There's no separate
# runner per combination to discover anymore (see runners/main/
# docs_search.py and page_links.py, which always use whichever adapter
# is configured as the default) — benchmarking every engine side by
# side means enumerating them here instead, the same "introspection use
# case" exception infrastructure/web_scraping/provider.py's own
# application-layer callers already rely on. Two adapter classes for
# httpx/curl_cffi (one per parser) since that comparison is the point
# of the heavy-page benchmark; one each for selenium/playwright, which
# can do both actions since an interactive adapter is-a reading one too.
_CANDIDATES: list[tuple[str, str, str, str, str, str]] = [
    (
        "infrastructure.framework.appcraft.templates.selenium",
        "SeleniumTemplate",
        "infrastructure.web_scraping.selenium.adapter",
        "SeleniumAdapter",
        "docs_search",
        "Selenium",
    ),
    (
        "infrastructure.framework.appcraft.templates.selenium",
        "SeleniumTemplate",
        "infrastructure.web_scraping.selenium.adapter",
        "SeleniumAdapter",
        "get_links",
        "Selenium",
    ),
    (
        "infrastructure.framework.appcraft.templates.playwright",
        "PlaywrightTemplate",
        "infrastructure.web_scraping.playwright.adapter",
        "PlaywrightAdapter",
        "docs_search",
        "Playwright",
    ),
    (
        "infrastructure.framework.appcraft.templates.playwright",
        "PlaywrightTemplate",
        "infrastructure.web_scraping.playwright.adapter",
        "PlaywrightAdapter",
        "get_links",
        "Playwright",
    ),
    (
        "infrastructure.framework.appcraft.templates.httpx",
        "HTTPXTemplate",
        "infrastructure.web_scraping.httpx.adapter",
        "HTTPXBeautifulSoupAdapter",
        "get_links",
        "HTTPXBeautifulSoup",
    ),
    (
        "infrastructure.framework.appcraft.templates.httpx",
        "HTTPXTemplate",
        "infrastructure.web_scraping.httpx.adapter",
        "HTTPXSelectolaxAdapter",
        "get_links",
        "HTTPXSelectolax",
    ),
    (
        "infrastructure.framework.appcraft.templates.curl_cffi",
        "CurlCffiTemplate",
        "infrastructure.web_scraping.curl_cffi.adapter",
        "CurlCffiBeautifulSoupAdapter",
        "get_links",
        "CurlCffiBeautifulSoup",
    ),
    (
        "infrastructure.framework.appcraft.templates.curl_cffi",
        "CurlCffiTemplate",
        "infrastructure.web_scraping.curl_cffi.adapter",
        "CurlCffiSelectolaxAdapter",
        "get_links",
        "CurlCffiSelectolax",
    ),
]


@dataclass
class BenchmarkInput:
    runs: int = 3
    urls: str = "https://example.com"


@dataclass
class BenchmarkResult:
    name: str
    elapsed_seconds: list[float] = field(default_factory=list)
    error: str | None = None

    @property
    def avg_seconds(self) -> float | None:
        if not self.elapsed_seconds:
            return None
        return sum(self.elapsed_seconds) / len(self.elapsed_seconds)


class BenchmarkWebScrapingRunnersUseCase(
    UseCase[BenchmarkInput, list[BenchmarkResult]]
):
    """Benchmarks every installed engine/parser/action combination
    (see _CANDIDATES) directly against its own adapter class — not
    through the generic docs_search/page_links runners, since those
    always resolve to whichever adapter is currently configured as the
    default, not every installed one.

    Each run happens in its own subprocess: browser/async state isn't
    safe to reuse or mix across different adapters in one process (e.g.
    Selenium's sync API and asyncio.run() calls for later httpx/curl_cffi
    runs corrupt each other in-process), and it keeps one adapter's
    overhead from bleeding into another's measurement.
    """

    def execute(self, input_data: BenchmarkInput) -> list[BenchmarkResult]:
        return [
            self._benchmark(
                adapter_module, adapter_class, action, label, input_data
            )
            for _, _, adapter_module, adapter_class, action, label in (
                self._discover_installed_candidates()
            )
        ]

    def _discover_installed_candidates(
        self,
    ) -> list[tuple[str, str, str, str, str, str]]:
        installed: list[tuple[str, str, str, str, str, str]] = []

        for candidate in _CANDIDATES:
            template_module_name, template_class_name = candidate[0:2]
            try:
                template_module = importlib.import_module(
                    template_module_name
                )
                template_class = getattr(
                    template_module, template_class_name
                )
                if template_class.is_installed():
                    installed.append(candidate)
            except Exception:
                continue

        return installed

    def _benchmark(
        self,
        adapter_module: str,
        adapter_class: str,
        action: str,
        label: str,
        input_data: BenchmarkInput,
    ) -> BenchmarkResult:
        name = f"{label}.{action}"
        script = (
            "import sys, os, json; "
            "sys.path.insert(0, os.getcwd()); "
            "from application.use_cases.web_scraping.benchmark import "
            "run_single_adapter_benchmark; "
            "print(json.dumps(run_single_adapter_benchmark("
            f"{adapter_module!r}, {adapter_class!r}, {action!r}, "
            f"{input_data.runs!r}, {input_data.urls!r})))"
        )

        try:
            process = subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                text=True,
                timeout=120,
            )
            output_line = process.stdout.strip().splitlines()[-1]
            data = json.loads(output_line)
        except Exception as e:
            return BenchmarkResult(name=name, error=str(e))

        return BenchmarkResult(
            name=data["name"],
            elapsed_seconds=data["elapsed_seconds"],
            error=data["error"],
        )


def _sync_call(adapter: Any, method_name: str, *args: Any, **kwargs: Any):
    method = getattr(adapter, method_name)
    if isinstance(adapter, WebScrapingAsyncPort):
        return asyncio.run(method(*args, **kwargs))
    return method(*args, **kwargs)


def run_single_adapter_benchmark(
    adapter_module: str,
    adapter_class: str,
    action: str,
    runs: int,
    urls: str,
) -> dict[str, Any]:
    """Runs in an isolated subprocess (see _benchmark above) — a fresh
    adapter instance per repetition.
    """
    result: dict[str, Any] = {
        "name": f"{adapter_class}.{action}",
        "elapsed_seconds": [],
        "error": None,
    }

    try:
        module = importlib.import_module(adapter_module)
        adapter_cls = getattr(module, adapter_class)

        for _ in range(runs):
            adapter = adapter_cls()
            _sync_call(adapter, "start", headless=True)

            start = time.perf_counter()
            if action == "docs_search":
                from application.use_cases.web_scraping.docs import (
                    SearchDocsUseCase,
                )

                SearchDocsUseCase(adapter).execute("Web Scraping")
            else:
                from application.use_cases.web_scraping.page_info import (
                    GetPageLinksUseCase,
                )

                GetPageLinksUseCase(adapter).execute([urls])
            result["elapsed_seconds"].append(time.perf_counter() - start)

            _sync_call(adapter, "finish")
    except Exception as e:
        result["error"] = str(e)

    return result
