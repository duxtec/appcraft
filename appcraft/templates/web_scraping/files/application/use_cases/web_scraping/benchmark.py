import importlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from application.use_cases import UseCase
from infrastructure.framework.appcraft.core.runner.discovery import (
    RunnerDiscovery,
)

# application/ normally depends only on domain/, but discovering "every
# scraping runner" is inherently an infrastructure-introspection concern
# (same reasoning as e.g. ListTablesUseCase importing SQLAlchemyAdapter
# directly) — RunnerDiscovery and WebScrapingRunnerBase both live in
# infrastructure/ specifically so this import doesn't have to reach into
# the runners/ layer instead.
from infrastructure.web_scraping.runner import WebScrapingRunnerBase

_RUNNER_FOLDERS = ("runners/main", "runners/tools")


@dataclass
class BenchmarkInput:
    runs: int = 3
    # Forwarded verbatim to each benchmarked runner method as kwargs
    # (e.g. {"urls": "https://example.com"}) — whichever ones a given
    # method doesn't recognize are simply unused, since every runner
    # method already accepts **kwargs.
    kwargs: dict[str, str] = field(default_factory=dict)


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
    """Benchmarks every discovered web-scraping Runner method — anything
    subclassing WebScrapingRunnerBase under runners/main or runners/tools
    that's concrete and @Runner.runner-decorated — instead of hardcoding
    a fixed action against a fixed set of adapters. A new scraping
    runner someone adds later is picked up the same way
    docs_search_selenium.Selenium.search_template_docs already is.

    Each run happens in its own subprocess: browser/async state isn't
    safe to reuse or mix across different runners in one process (e.g.
    Selenium's sync API and asyncio.run() calls for later httpx/curl_cffi
    runs corrupt each other in-process), and it keeps one runner's
    overhead from bleeding into another's measurement.
    """

    def execute(self, input_data: BenchmarkInput) -> list[BenchmarkResult]:
        return [
            self._benchmark(module_name, class_name, method_name, input_data)
            for module_name, class_name, method_name in (
                self._discover_scraping_runners()
            )
        ]

    def _discover_scraping_runners(self) -> list[tuple[str, str, str]]:
        candidates: list[tuple[str, str, str]] = []

        for folder in _RUNNER_FOLDERS:
            if not os.path.isdir(folder):
                continue

            module_prefix = folder.replace("/", ".")
            for module_name in RunnerDiscovery.get_modules(folder):
                full_module_name = f"{module_prefix}.{module_name}"
                try:
                    module = importlib.import_module(full_module_name)
                except Exception:
                    continue

                for app in RunnerDiscovery.get_apps(module):
                    if not issubclass(app, WebScrapingRunnerBase):
                        continue

                    for method_name in RunnerDiscovery.get_app_runners(app):
                        candidates.append(
                            (full_module_name, app.__name__, method_name)
                        )

        return candidates

    def _benchmark(
        self,
        module_name: str,
        class_name: str,
        method_name: str,
        input_data: BenchmarkInput,
    ) -> BenchmarkResult:
        name = f"{class_name}.{method_name}"
        script = (
            "import sys, os, json; "
            "sys.path.insert(0, os.getcwd()); "
            "from application.use_cases.web_scraping.benchmark import "
            "run_single_runner_benchmark; "
            "print(json.dumps(run_single_runner_benchmark("
            f"{module_name!r}, {class_name!r}, {method_name!r}, "
            f"{input_data.runs!r}, {input_data.kwargs!r})))"
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


def run_single_runner_benchmark(
    module_name: str,
    class_name: str,
    method_name: str,
    runs: int,
    kwargs: dict[str, str],
) -> dict[str, Any]:
    """Runs in an isolated subprocess (see _benchmark above) — a fresh
    instance of the runner per repetition, matching how a real
    `python run_tools ...` invocation always starts fresh too.
    """
    result: dict[str, Any] = {
        "name": f"{class_name}.{method_name}",
        "elapsed_seconds": [],
        "error": None,
    }

    try:
        module = importlib.import_module(module_name)
        app_cls = getattr(module, class_name)

        for _ in range(runs):
            instance = app_cls()
            method = getattr(instance, method_name)

            start = time.perf_counter()
            method(**kwargs)
            result["elapsed_seconds"].append(time.perf_counter() - start)
    except Exception as e:
        result["error"] = str(e)

    return result
