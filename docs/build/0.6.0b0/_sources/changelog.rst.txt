Changelog
=============================

Formal changelog tracking starts with 0.6.0 — for anything earlier, see the `commit history <https://github.com/duxtec/appcraft/commits/main/>`_ on GitHub.

0.6.0b0
----------

Added
~~~~~~~~

- ``docker`` template activated: a single Dockerfile (installs through whichever package manager is active, non-root user, skips dev-only deps in production) and a ``docker-compose.yml`` generated automatically from every deployable runner.
- ``mongodb`` template.
- ``pipenv``/``uv`` package-manager templates, swappable with ``poetry`` at any time (``appcraft init uv`` or ``appcraft add_template pipenv``), converting existing dependencies along the way.
- ``web_scraping`` rebuilt as a shared base template with interchangeable engine adapters (``selenium``, ``playwright``, ``httpx``, ``curl_cffi``), including session handoff between an interactive (browser) engine and a faster reading-only one.
- ``AGENTS.md`` as the canonical, cross-tool project-instructions file (also read by Cursor, GitHub Copilot, Windsurf, Codex, and others), with ``CLAUDE.md`` importing it for full Claude Code semantics.
- Documentation moved to the repository root and versioned (``docs/<version>/``), with a version-selector page.
- This Changelog and a Contact page.
- ``LICENSE`` file (the project has always been MIT-licensed per its package metadata; the license text itself was missing).

Changed
~~~~~~~~

- ``sqlalchemy`` adapter rebuilt around ``DatabasePort``/ports/use-cases; the stale, unused ``App`` ORM model removed.
- ``flask`` split into a shared, non-standalone base plus ``flask_api``/``flask_ui``, composed via ``is_installed()`` instead of template-generation-time branching.
- Package-manager ownership of ``pyproject.toml`` moved to ``base``; ``poetry`` demoted from a hard dependency to a swappable (still default) template.
- Database/web-scraping ``Provider`` functions (``get_default_database_adapter()``, ``get_default_interactive_adapter()``, etc.) moved from ``application/providers/`` to ``infrastructure/<concept>/provider.py``, correcting an ``application`` → ``infrastructure`` layering inversion.
- ``web_scraping`` runners consolidated: one shared ``docs_search``/``page_links`` runner per action (default adapter picked via config or direct injection) instead of one runner per engine.
- ``Repository``/``RepositoryBase`` now derive ``model``/``new_model`` automatically from their generic subscript, matching how ``BaseMapper`` already derived ``model``/``schema`` — a concrete repository no longer redeclares either.
- Pydantic usage inside ``domain/`` centralized to a single file (``domain/models/core/pydantic.py``); every other ``domain/`` file imports Pydantic-derived names from there instead of ``pydantic`` directly, so dropping Pydantic later (e.g. for a MicroPython target) only means rewriting that one file.

Fixed
~~~~~~~~

- ``appcraft init <package-manager>``-triggered template swaps (e.g. ``appcraft init uv`` on a fresh project) crashing on a ``str``/``Path`` mismatch.
- ``HTTPXAdapter``: ``RuntimeError: Event loop is closed`` raised from ``finish()`` when driven by synchronous code (a runner, or the benchmark tool).
- ``init``/``add_template --help`` text hardcoding an outdated default-template list.
- ``SearchDocsUseCase`` not actually working against async (Playwright) adapters despite its typing suggesting it did.
- A broken "Contribute" link in this README.

Removed
~~~~~~~~

- ``git``/``github`` templates deactivated pending migration off the pre-``Port``/``use_cases`` architecture (they still work, just hidden from ``list_templates``/``init`` unless ``--install-inactive`` is passed).
- ``locales``/``logs`` templates deactivated (their dependencies were declared Pipfile-only, so a default Poetry project silently never installed them).
- Per-engine ``web_scraping`` runner files and several dead, unused type aliases left over from before the runner consolidation above.
