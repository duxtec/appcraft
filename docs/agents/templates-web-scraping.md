# Web scraping templates (`web_scraping`, `selenium`, `playwright`, `httpx`, `curl_cffi`)

Combines both variants of the [interchangeable-sibling-adapters pattern](architecture.md#the-interchangeable-sibling-adapters-via-is_installed-pattern): a shared non-`standalone` base template like `flask`'s (since the `Port` and domain contracts are scraping-specific, not part of `base`), *and* true interchangeable engines like `sqlalchemy`/`mongodb`'s — plus a mechanism neither of those two families needs: runtime session handoff between two different installed adapters.

## `web_scraping` (active, `standalone = False`)

The shared foundation — install one or more of `selenium`/`playwright`/`httpx`/`curl_cffi` instead; `web_scraping` itself is rejected if requested directly.

### Domain layer

- `domain/html_elements/interface/__init__.py` — a 4-level interface hierarchy distinguishing what an engine can do, enforced by pyright via generic bounds rather than an explicit marker type:
  `HTMLElementInterface` → `HTMLReadingElementInterface` (`inner_html`/`inner_text`/`has_attribute`/`get_attribute`) → `HTMLNavigationElementInterface` (+ `query_selector`/`query_selector_all`/`children`, returning `Sequence[Self]` — not `list[Self]`, since `list` is invariant and would break a subclass returning a narrower element type) → `HTMLInteractiveElementInterface` (+ `set`/`add`/`remove_attribute`, `append_child`/`remove_child`, `send_keys`, `click`/`hover`/`focus`/`blur`/`remove`). Only real browsers (`selenium`, `playwright`) can produce `HTMLInteractiveElementInterface` instances; HTTP-only engines (`httpx`, `curl_cffi`) top out at `HTMLReadingElementInterface`.
- `domain/web_scraping/cookie.py` — `Cookie` frozen dataclass.
- `domain/web_scraping/session.py` — `WebScrapingSession` frozen dataclass (`cookies: list[Cookie]`, `headers: dict[str, str]`).
- `domain/exceptions/web_scraping.py` — `WebScrapingException`, `NoSuchElementException`, `BrowserNotInstalledException`, `NoBrowsersInstalledException`.

### Application layer

- `application/ports/web_scraping.py` — `WebScrapingPort[THTMLElement]` / `WebScrapingAsyncPort[THTMLElement]`, both abstract: `start`, `finish`, `open_page`, `query_selector`, `query_selector_all`, `get_cookies`/`set_cookies`, `get_headers`/`set_headers`. A concrete adapter is sync (`selenium`, `httpx`, `curl_cffi` — httpx/curl_cffi wrap their own async client internally but expose a sync `Port`) or async (`playwright`); code that holds one polymorphically must `isinstance`-branch on `WebScrapingAsyncPort` before calling any method, since an un-checked call on the async variant silently produces an un-awaited coroutine instead of a real value (pyright catches this).
- `application/providers/adapters/web_scraping.py`:
  - `get_default_interactive_adapter()` — the default browser-automation adapter. `_INTERACTIVE_BACKENDS` maps `"playwright"`/`"selenium"` the same way `database.py`'s `_ADAPTER_BACKENDS` does; `config/web_scraping.toml`'s `default_interactive_adapter` breaks the tie. Returns `None` if neither is installed.
  - `get_default_reading_adapter()` — the default read-only adapter. Tries `_READING_BACKENDS` (`"httpx"`/`"curl_cffi"`, `config/web_scraping.toml`'s `default_reading_adapter`) first; if neither is installed, falls back to `get_default_interactive_adapter()` (the *same cached instance*), since `HTMLInteractiveElementInterface` is itself a `HTMLReadingElementInterface` — a browser can do everything a read-only adapter can.
  - `delegate_to_reading_adapter(interactive)` — call once the interactive-only part of a flow is done (login, solving a JS challenge, etc). Returns `get_default_reading_adapter()` with `interactive`'s session (cookies + headers, via `get_session()`/`set_session()`) already copied over — or `interactive` itself, unchanged, if `reading is interactive` (same adapter, nothing to copy). Closes `interactive` when handing off to a genuinely different adapter, and safely clears the module-level cached-default slot only if `interactive` *was* the cached instance (so a later `get_default_interactive_adapter()` call doesn't hand out a dead adapter).
- `application/use_cases/web_scraping/`:
  - `docs.py` — `SearchDocsUseCase(UseCase[str, list[HTMLInteractiveElementInterface]])`, requires an interactive adapter.
  - `page_info.py` — `GetPageLinksUseCase`, works with any reading-or-better adapter; `TLink = HTMLReadingElementInterface | dict[str, str | None]`.
  - `delegate_session.py` — `DelegateSessionUseCase`, the example flow described below.
  - `benchmark.py` — `BenchmarkWebScrapingRunnersUseCase`, described below. Imports `RunnerDiscovery` and `WebScrapingRunnerBase` directly from `infrastructure/` — the accepted `application/` → `infrastructure/` introspection exception from [architecture.md](architecture.md#naming-and-layering-conventions), since discovering "every installed scraping runner" is inherently an infra-introspection concern.

### Infrastructure layer

- `infrastructure/web_scraping/adapter.py` — `WebScrapingAdapterBase`/`WebScrapingAsyncAdapterBase`: concrete `headless`/`timeout` properties, `start()`, and **concrete** `get_session()`/`set_session()` composed from each engine's abstract cookie/header primitives. (`Port` = pure contract, `*AdapterBase` = composed conveniences shared by every concrete engine — the same split `DatabasePort`/`MemoryAdapter` don't need since there's only ever one concrete adapter per engine there, but is worth keeping in mind for any future multi-engine `Port`.)
- `infrastructure/web_scraping/runner.py` — `WebScrapingRunnerBase[TAdapter]` (uses [`PropertyMeta`](architecture.md#the-runner-system) to derive the concrete adapter class from a generic subscript) plus `WebScrapingReaderRunnerBase`/`WebScrapingNavigationRunnerBase`/`WebScrapingInteractiveRunnerBase`. Lives in `infrastructure/`, not `runners/`, specifically so `application/`'s benchmark use case can import it without depending on the `runners/` layer.
- `infrastructure/web_scraping/parser/{interface,bs4,selectolax}.py` — `HTMLParserInterface` + `BeautifulSoupParser`/`SelectolaxParser`, a composition-based parsing strategy shared by the `httpx` and `curl_cffi` engines (each ships its own byte-identical copy, deliberately, to keep templates independent — see the engines below).
- `infrastructure/web_scraping/types/{adapters,html_elements}.py` — `TypeVar`s bound to the `Port`/`Interface` types, used by the generic runner bases and `application/providers/adapters/web_scraping.py`'s `TInteractiveAdapter`/`TReadingAdapter` aliases.
- `infrastructure/web_scraping/utils/keys.py` — `Keys`, WebDriver-style Unicode PUA special-key codes shared by Selenium's and Playwright's `send_keys` implementations.

### Presentation / runners

- `presentation/cli/web_scraping/{docs,page_info,benchmark,delegate_session}.py` — one `<Domain>CLIPresentation` class per use case, following the convention in [architecture.md](architecture.md#naming-and-layering-conventions).
- `runners/main/docs_search.py` / `page_links.py` — abstract `DocsSearchRunnerBase`/`PageLinksRunnerBase`; each engine template subclasses these with itself as the generic argument (e.g. `class Selenium(Runner, DocsSearchRunnerBase[SeleniumAdapter]): pass`) to get a concrete, discoverable `Runner` in one line.
- `runners/tools/benchmark.py` — `WebScrapingBenchmark(Runner)`. `run()`/`run_heavy_page()` both call `_discover_scraping_runners()` (via `RunnerDiscovery`, filtered to `WebScrapingRunnerBase` subclasses under `runners/main`+`runners/tools`) then benchmark *every* discovered `@Runner.runner` method — not a hardcoded adapter list, so a new scraping runner someone adds later is picked up automatically. Each repetition runs in its own subprocess (`subprocess.run([sys.executable, "-c", ...])`) with a fresh runner instance: Playwright's sync API corrupts a process's `asyncio` state for any later `asyncio.run()` call (e.g. a subsequent httpx/curl_cffi run in the same process), and Playwright itself refuses a second `sync_playwright().start()` per process if a prior instance wasn't `.stop()`-ed. `run_heavy_page()` defaults `urls` to `https://html.spec.whatwg.org/` (~15MB) and bumps repetitions, isolating parser/engine speed from the network-latency noise a small page introduces.
- `runners/tools/delegate_session.py` — `DelegateSession(Runner)`, an example flow: starts the default interactive adapter, sets a cookie (stand-in for a login/JS challenge), calls `delegate_to_reading_adapter()`, then confirms the handoff by comparing `get_cookies()` on each adapter before/after — not by parsing the response body, since some parser/URL combinations don't reliably produce a `<body>` for non-HTML content (BeautifulSoup's `html.parser` backend doesn't synthesize one; `selectolax` does).

### `config/web_scraping.toml`

`default_interactive_adapter = "playwright"`, `default_reading_adapter = "httpx"` — read by the provider functions above.

## `selenium` (active, `dependencies = ["web_scraping"]`)

`infrastructure/web_scraping/selenium/{adapter,html_element}.py` — `SeleniumAdapter`, `SeleniumHTMLElement`. Picks a browser via `browser_manager`/`webdriver_manager`, checking `.is_installed` on an *instance* (not the class — that returns the property descriptor object, always truthy). `get_headers()`/`set_headers()` use CDP (`execute_cdp_cmd`) when available; `User-Agent` is always readable via `driver.execute_script("return navigator.userAgent")`. `runners/main/docs_search_selenium.py`/`page_links_selenium.py` are one-line concrete runners.

## `playwright` (active, `dependencies = ["web_scraping"]`, `post_install` runs `playwright install chromium`)

`infrastructure/web_scraping/playwright/{adapter,html_element}.py` — `PlaywrightAdapter`, async. `finish()` must call both `self._browser.close()` **and** `self._playwright.stop()` — omitting the latter leaves the sync-API "already in use" guard tripped for the next `PlaywrightAdapter()` in the same process. `set_extra_http_headers` *replaces* the whole header set rather than merging, so `set_headers()` re-merges `self._headers` in full on every call.

## `httpx` (active, `dependencies = ["web_scraping"]`)

`infrastructure/web_scraping/httpx/adapter.py` — `HTTPXAdapter(parser: HTMLParserInterface)` composed with a parser (not subclassed per parser); `HTTPXBeautifulSoupAdapter`/`HTTPXSelectolaxAdapter` are one-line subclasses fixing the parser choice. Cookies/headers via `self.client.cookies.jar` / `.cookies.set(name, value, domain=, path=)` / `.headers` (a real mutable dict-like). `infrastructure/web_scraping/parser/` — see the shared parser strategy above.

## `curl_cffi` (active, `dependencies = ["web_scraping"]`)

`infrastructure/web_scraping/curl_cffi/adapter.py` — `CurlCffiAdapter(parser: HTMLParserInterface)`, same composed-parser shape as `httpx`'s, with an `_ensure_client()` helper factoring out lazy `AsyncSession` construction. Same cookie/header shape as `httpx` (`client.cookies.jar`/`.set()`/`.headers`, since both wrap `http.cookiejar.Cookie`-compatible objects).

**Why this exists alongside `httpx`**: not for speed (the two are effectively equivalent — see the benchmark numbers below) but for TLS/JA3 fingerprinting. `httpx`'s handshake looks like plain Python/OpenSSL, easily flagged by anti-bot protection (Cloudflare, Akamai, etc); `curl_cffi` wraps `curl-impersonate` to mimic a real browser's TLS/HTTP2 fingerprint. Pick `httpx` by default; reach for `curl_cffi` specifically when a target site blocks on fingerprint.

## Measured benchmark data (2026-09-20/21, this sandbox)

Light page (`https://example.com`, 10 runs) — `httpx`/`curl_cffi` are near-identical regardless of parser (~0.04-0.05s avg); `Playwright` (Chromium headless-shell) beats `Selenium` (Firefox headless) by roughly an order of magnitude on both actions tested. Every browser-based runner's *first* run in a fresh process is a multi-second outlier (browser/driver startup) — median, not mean, reflects steady-state cost once warmed up (e.g. `Selenium.search_template_docs`: mean 7.29s pulled up by a single 32.9s outlier run, median 3.33s).

Heavy page (`https://html.spec.whatwg.org/`, ~15MB, 8 runs, `httpx`/`curl_cffi` only — browsers were never benchmarked against it) — `selectolax` beats `BeautifulSoup` by ~5.6x end-to-end (fetch+parse+extract-links: ~2.3-2.5s vs ~13.2-13.4s); a separate raw-parse-only micro-benchmark on the same fetched text (no network) showed selectolax ~23x faster than BeautifulSoup for parsing alone (0.44s vs 9.91s) — the gap narrows end-to-end because network fetch time and per-element Python-object overhead dilute the raw parsing advantage.
