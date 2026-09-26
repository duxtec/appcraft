Web Scraping Template
=============================

The **Web Scraping Template** is the shared foundation for extracting data from websites — it can't be installed by itself (``standalone = False``); install one or more of `Selenium <../selenium/index.html>`_, `Playwright <../playwright/index.html>`_, `HTTPX <../httpx/index.html>`_, or `curl_cffi <../curl_cffi/index.html>`_ instead, each of which depends on this one.

These four engines are **freely combinable, not exclusive** — a project can use ``httpx`` for static pages and ``playwright`` for JS-heavy ones side by side, or install every engine at once. This template provides everything they share: the abstract contract they all implement, the domain types pages are exposed through, and generic use cases/runners built on top.

What this template provides
------------------------------

- **``WebScrapingPort`` / ``WebScrapingAsyncPort``** (``application/ports/web_scraping.py``) — the contract every engine implements: ``start``, ``finish``, ``open_page``, ``query_selector``, ``query_selector_all``, plus session primitives (``get_cookies``/``set_cookies``, ``get_headers``/``set_headers``). Sync engines (Selenium, HTTPX, curl_cffi) implement ``WebScrapingPort``; Playwright, being natively async, implements ``WebScrapingAsyncPort``.
- **A 4-level HTML element hierarchy** (``domain/html_elements/interface/``) distinguishing what an engine can actually do with a page: reading text/attributes, navigating the DOM tree, and — only for real browsers — interacting with it (clicking, typing, filling forms). Selenium and Playwright produce fully interactive elements; HTTPX and curl_cffi, having no browser, produce read-only ones. This distinction is enforced by the type system itself, not by a runtime flag.
- **Session sharing** (``domain/web_scraping/{cookie,session}.py``, plus ``get_session()``/``set_session()`` on every adapter) — see `Handing off between engines`_ below.
- **Generic use cases and runners** — searching a page (``SearchDocsUseCase``, needs an interactive engine), extracting every link on a page (``GetPageLinksUseCase``, works with any engine), and a benchmark tool (see `Benchmarking installed engines`_).

Choosing an engine
--------------------

- **Selenium** — needs a browser. Broad browser support, mature ecosystem.
- **Playwright** — needs a browser. Modern JS-heavy sites; faster than Selenium.
- **HTTPX** — no browser needed. Fast, simple pages with no JS rendering required.
- **curl_cffi** — no browser needed. Same as HTTPX, plus bypassing TLS/fingerprint-based anti-bot protection.

If a page needs JavaScript execution (clicking, scrolling, waiting for content to load), you need Selenium or Playwright. Otherwise, HTTPX is the simpler default — reach for curl_cffi specifically when a target site blocks plain HTTP clients by their TLS handshake fingerprint.

Handing off between engines
------------------------------

A common pattern: use a browser to do something only a browser can (log in, solve a JS challenge), then switch to a much faster HTTP client for the rest of the scrape — without losing the session. ``infrastructure/web_scraping/provider.py`` provides this:

- ``get_default_interactive_adapter()`` — the configured browser engine (``config/web_scraping.toml``'s ``default_interactive_adapter``), or whichever of Selenium/Playwright is installed.
- ``get_default_reading_adapter()`` — the configured fast engine (``default_reading_adapter``), falling back to the interactive one if no HTTP-only engine is installed.
- ``delegate_to_reading_adapter(interactive)`` — copies cookies and headers from the interactive adapter's session onto the reading adapter, closes the interactive one, and returns the reading adapter ready to continue. If both defaults resolve to the same engine, it's a no-op — the flow just continues on the one adapter.

The ``delegate_session`` tool runner (below) demonstrates the whole flow end to end.

Available runners
--------------------

There's a single ``docs_search`` and a single ``page_links`` runner, provided by this template — not one per engine. Both use whichever adapter is currently configured as the default:

- ``search_template_docs`` (``python run docs_search``) — searches for text on a page, using the default *interactive* engine (``get_default_interactive_adapter()``).
- ``get_links`` (``python run page_links``) — extracts every link on a page, using the default *reading* engine (``get_default_reading_adapter()``).

To use a different engine than the current default, either change ``config/web_scraping.toml``'s ``default_interactive_adapter``/``default_reading_adapter``, or — for code that needs one specific engine regardless of that setting — inject its concrete adapter class directly (e.g. ``SeleniumAdapter()``, ``HTTPXSelectolaxAdapter()``) into your own use case instead of going through these runners. See `Choosing an engine`_.

Two more tool runners round out the template:

- ``python run_tools benchmark run`` / ``run_heavy_page`` — times every *installed* engine (not just the current default) against a light page (``example.com``) or a large one (~15MB), respectively. See `Benchmarking installed engines`_.
- ``python run_tools delegate_session`` — the interactive-to-reading handoff example above.

Benchmarking installed engines
---------------------------------

The benchmark tool checks a fixed list of known engine/parser/action combinations against ``is_installed()`` and times whichever ones are actually present in the project — so installing a new engine gets it included automatically, with no configuration needed. Measured results from this project's own testing:

**Light page** (``example.com``, 10 runs): HTTPX and curl_cffi are near-identical regardless of parser (~0.04–0.05s average). Playwright beats Selenium by roughly an order of magnitude. Every browser-based run's *first* execution in a fresh process is a multi-second outlier (browser startup cost) — worth using the median, not the mean, to judge steady-state performance.

**Heavy page** (the ~15MB WHATWG HTML spec, 8 runs, HTTPX/curl_cffi only): ``selectolax`` beats ``BeautifulSoup`` by about 5.6× end to end (fetch + parse + extract links: ~2.3–2.5s vs ~13.2–13.4s). Isolating just the parsing step (same downloaded text, no network) widens that to ~23× — the end-to-end gap narrows because network time and per-element Python object overhead dilute the raw parsing advantage.
