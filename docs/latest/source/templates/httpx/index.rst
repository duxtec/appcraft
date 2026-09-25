HTTPX Template
=============================

The **HTTPX Template** implements the `Web Scraping Template <../web_scraping/index.html>`_'s ``WebScrapingAsyncPort`` on top of **HTTPX**, a fast async HTTP client — no browser involved, for pages that don't need JavaScript execution.

It depends on ``web_scraping`` (installed automatically) and is combinable with the other engines (``selenium``, ``playwright``, ``curl_cffi``) — install whichever this project needs side by side.

Choosing a parser
--------------------

HTTPX itself only fetches pages — parsing HTML is handled by a separate, swappable parser: **BeautifulSoup** or **selectolax**. Two ready-made adapter classes cover both (``HTTPXBeautifulSoupAdapter``, ``HTTPXSelectolaxAdapter``), sharing the exact same HTTP-fetching logic and differing only in which parser they compose.

In this project's own benchmarks on a large page, selectolax beat BeautifulSoup by roughly 5.6× end to end — see the `Web Scraping Template <../web_scraping/index.html#benchmarking-installed-engines>`_ page for the numbers. selectolax is the better default unless a specific BeautifulSoup feature is needed.

Cookies and headers
----------------------

Both work through HTTPX's own client — cookies via its cookie jar, headers via its own mutable header dict. This is what makes `session handoff <../web_scraping/index.html#handing-off-between-engines>`_ from a browser engine to HTTPX possible.

Using HTTPX specifically
---------------------------

This template doesn't add its own runners — the `Web Scraping Template <../web_scraping/index.html>`_'s ``page_links`` runner already works once HTTPX is installed. To make HTTPX the one actually used, either set it as the default (``config/web_scraping.toml``'s ``default_reading_adapter``, e.g. ``"httpx_selectolax"``) or inject ``HTTPXBeautifulSoupAdapter``/``HTTPXSelectolaxAdapter`` directly in your own code to pick the parser explicitly. See `Available runners <../web_scraping/index.html#available-runners>`_.
