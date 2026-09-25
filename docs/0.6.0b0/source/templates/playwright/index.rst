Playwright Template
=============================

The **Playwright Template** implements the `Web Scraping Template <../web_scraping/index.html>`_'s ``WebScrapingAsyncPort`` on top of **Playwright**, for full browser automation across Chromium, Firefox, and WebKit.

It depends on ``web_scraping`` (installed automatically) and is combinable with the other engines (``selenium``, ``httpx``, ``curl_cffi``) — install whichever this project needs side by side. On install, it automatically runs ``playwright install chromium`` so a working browser is ready immediately.

Async by nature
------------------

Unlike Selenium, Playwright's Python API is natively asynchronous — this engine implements ``WebScrapingAsyncPort``, not the sync ``WebScrapingPort``. Code that works with an engine polymorphically (not knowing in advance which one it got) needs to check which contract it's dealing with and ``await`` accordingly; see `handing off between engines <../web_scraping/index.html#handing-off-between-engines>`_ for the pattern used throughout this codebase.

In this project's own benchmarks, Playwright was consistently around an order of magnitude faster than Selenium for equivalent actions — see the `Web Scraping Template <../web_scraping/index.html#benchmarking-installed-engines>`_ page.

Cookies and headers
----------------------

Playwright's own APIs handle cookies and headers directly. One notable detail: setting extra HTTP headers *replaces* the whole header set rather than merging into it, so this adapter always re-applies the full tracked header dictionary on every change — not just the new value.

Using Playwright specifically
---------------------------------

This template doesn't add its own runners — the `Web Scraping Template <../web_scraping/index.html>`_'s ``docs_search``/``page_links`` runners already work once Playwright is installed. To make Playwright the one actually used, either set it as the default (``config/web_scraping.toml``'s ``default_interactive_adapter = "playwright"``) or inject ``PlaywrightAdapter`` directly in your own code. See `Available runners <../web_scraping/index.html#available-runners>`_.
