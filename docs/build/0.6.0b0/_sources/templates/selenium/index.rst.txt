Selenium Template
=============================

The **Selenium Template** implements the `Web Scraping Template <../web_scraping/index.html>`_'s ``WebScrapingPort`` on top of **Selenium WebDriver**, for full browser automation — JavaScript execution, clicking, form input, scrolling, and everything else a real browser can do.

It depends on ``web_scraping`` (installed automatically) and is combinable with the other engines (``playwright``, ``httpx``, ``curl_cffi``) — install whichever this project needs side by side.

Browser detection
--------------------

Selenium picks a browser automatically via ``browser_manager``/``webdriver_manager``, based on what's actually installed on the machine — there's no manual driver setup required.

Cookies and headers
----------------------

``get_cookies()``/``set_cookies()`` work through Selenium's own cookie API. ``get_headers()``/``set_headers()`` use the Chrome DevTools Protocol (via ``execute_cdp_cmd``) when the underlying browser supports it; the current ``User-Agent`` is always readable regardless, via a small JavaScript snippet run in the page. This is what makes `session handoff <../web_scraping/index.html#handing-off-between-engines>`_ to a faster engine possible.

Using Selenium specifically
-------------------------------

This template doesn't add its own runners — the `Web Scraping Template <../web_scraping/index.html>`_'s ``docs_search``/``page_links`` runners already work once Selenium is installed. To make Selenium the one actually used, either set it as the default (``config/web_scraping.toml``'s ``default_interactive_adapter = "selenium"``) or inject ``SeleniumAdapter`` directly in your own code. See `Available runners <../web_scraping/index.html#available-runners>`_.
