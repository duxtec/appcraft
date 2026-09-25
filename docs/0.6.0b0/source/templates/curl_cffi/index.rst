curl_cffi Template
=============================

The **curl_cffi Template** implements the `Web Scraping Template <../web_scraping/index.html>`_'s ``WebScrapingAsyncPort`` on top of **curl_cffi** — like `HTTPX <../httpx/index.html>`_, no browser involved, paired with the same choice of **BeautifulSoup** or **selectolax** for parsing.

It depends on ``web_scraping`` (installed automatically) and is combinable with the other engines (``selenium``, ``playwright``, ``httpx``) — install whichever this project needs side by side.

Why this exists alongside HTTPX
----------------------------------

Not for speed — in this project's own benchmarks, curl_cffi and HTTPX performed near-identically. The reason to reach for curl_cffi specifically is **TLS/JA3 fingerprinting**: HTTPX's TLS handshake looks like plain Python/OpenSSL, which anti-bot protection (Cloudflare, Akamai, and similar) can detect and block. curl_cffi wraps ``curl-impersonate`` to mimic a real browser's TLS and HTTP/2 fingerprint instead, getting past that kind of protection.

Use HTTPX by default; switch to curl_cffi specifically when a target site is blocking your requests based on fingerprint rather than behavior.

Cookies and headers
----------------------

Same shape as HTTPX — both wrap ``http.cookiejar``-compatible cookie objects and expose a real mutable header dict, so `session handoff <../web_scraping/index.html#handing-off-between-engines>`_ between the two (or from a browser engine) works the same way.

Using curl_cffi specifically
---------------------------------

This template doesn't add its own runners — the `Web Scraping Template <../web_scraping/index.html>`_'s ``page_links`` runner already works once curl_cffi is installed. To make curl_cffi the one actually used, either set it as the default (``config/web_scraping.toml``'s ``default_reading_adapter``, e.g. ``"curl_cffi_selectolax"``) or inject ``CurlCffiBeautifulSoupAdapter``/``CurlCffiSelectolaxAdapter`` directly in your own code to pick the parser explicitly. See `Available runners <../web_scraping/index.html#available-runners>`_.
