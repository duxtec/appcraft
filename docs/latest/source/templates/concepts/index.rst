Template Types
=================

Before picking which templates to install, it helps to know that not all templates relate to each other the same way. Some are always there, some only make sense combined with others, some replace each other, and some are meant to be mixed freely. This page explains those relationships so the per-template pages that follow make sense in context.

Default Templates
--------------------

A handful of templates are **always included**, whether you name them or not:

.. code-block:: bash

    appcraft init
    # is equivalent to
    appcraft init base poetry

``base`` and ``poetry`` fall into this category today — running ``appcraft init`` with no arguments at all already gives you a complete, working project. Any templates you *do* name get added on top of these.

Shared-Base Templates
------------------------

Some templates exist only to be depended on by others, and **can't be installed by name directly**:

.. code-block:: bash

    appcraft init flask
    # ❌ Error: The template 'flask' cannot be installed standalone —
    #    it is only usable as a dependency of another template.
    #    Install one of these instead: flask_api, flask_ui.

``flask`` (shared by ``flask_api``/``flask_ui``) and ``web_scraping`` (shared by ``selenium``/``playwright``/``httpx``/``curl_cffi``) work this way — they hold the setup their sibling templates all need, but have nothing useful to offer on their own. Installing any sibling pulls its shared base in automatically:

.. code-block:: bash

    appcraft init flask_api
    # installs both 'flask' and 'flask_api'

Exclusive Templates
----------------------

A few templates are **mutually exclusive alternatives** — installing one *replaces* whichever other member of the same group was active, rather than sitting alongside it. The package managers (``poetry``, ``pipenv``, ``uv``) work this way:

.. code-block:: bash

    appcraft init poetry pipenv
    # ❌ Error: Cannot install poetry, pipenv together — they all
    #    belong to the 'package_manager' exclusive group, only one
    #    of them can be installed at a time.

Requesting two of them **together** is an error, as above. Requesting one when a *different* one is already installed is fine — it's a deliberate swap, and it works the same way whether you're changing an existing project or asking for it up front on a brand new one:

.. code-block:: bash

    appcraft add_template pipenv
    # on an existing project: switches it from whatever package manager
    # it had (e.g. poetry) to pipenv, converting the existing
    # dependencies along the way — not just adding pipenv alongside it

    appcraft init uv
    # on a brand new project: poetry is installed first as usual (it's
    # a default template), then immediately swapped for uv in the same
    # command — you never end up with both, even though only 'uv' was
    # named explicitly

Interchangeable Templates
-----------------------------

Unlike exclusive templates, some sibling templates can be **installed together and both stay fully usable** — a project setting picks which one backs the generic default, but the other remains directly available. The database engines (``sqlalchemy``, ``mongodb``) and the web scraping engines (``selenium``, ``playwright``, ``httpx``, ``curl_cffi``) both work this way:

.. code-block:: bash

    appcraft init sqlalchemy mongodb
    # both are installed and usable; config/app.toml's
    # default_database_adapter picks which one the generic
    # "default" database calls use

    appcraft init selenium httpx
    # a project can use a real browser (selenium) for pages that
    # need it, and a fast HTTP client (httpx) for everything else

There's no error for requesting several of these together — they're designed to coexist.

Composable Extensions
------------------------

A variant of the shared-base pattern, without a "pick one default" question at all: each sibling just toggles on a feature, and any combination is valid. ``flask_api`` and ``flask_ui`` are the example — install one, the other, or both on top of the shared ``flask`` template, and each is independently active:

.. code-block:: bash

    appcraft init flask_api flask_ui
    # a single project serving both a JSON API and rendered web pages

Dependencies
--------------

Beyond the categories above, any template can simply declare that it needs another one installed first — ``github`` requires ``git``, every web scraping engine requires ``web_scraping``, and so on. You don't need to list these yourself; requesting the dependent template installs its dependencies automatically, in the right order.

Inactive Templates
---------------------

Some templates exist in the codebase but aren't ready — or, for ``git``/``github`` specifically, are temporarily paused pending internal rework (see their own pages for why). These don't show up in ``appcraft list_templates`` and are rejected by ``init``/``add_template`` unless you pass ``--install-inactive`` explicitly:

.. code-block:: bash

    appcraft init git --install-inactive

Treat this flag as an explicit "I know this isn't fully ready" opt-in, not a normal part of setting up a project.
