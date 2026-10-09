.. _contributing:

Contributing
============

We appreciate your interest in contributing! The source lives at `github.com/duxtec/appcraft <https://github.com/duxtec/appcraft>`_. You can contribute in three ways:

1. `Creating New Templates`_.
2. `Updating Existing Templates`_.
3. `Translating the Framework`_.

Not sure what to work on yet? See `Looking for Something to Build?`_ below for ideas, then come back to whichever of the three fits what you picked.

Looking for Something to Build?
--------------------------------

Not every template is finished, and the framework itself has a few open gaps. Pick one of these if you don't already have something in mind — each links to the contribution path it follows.

**Finish a scaffolded template.** These ship real files but stay ``active = False`` until someone verifies them end to end, so this is `Updating Existing Templates`_, not a new one:

- ``locales`` and ``logs`` each declare their real dependencies (``polib``; ``structlog``) correctly in a ``pyproject.toml`` fragment and install fine on a default Poetry project — that part's done. What's missing is full behavioral verification: translation switching for ``locales``, log rotation beyond a smoke test for ``logs``. Verify end to end, then flip ``active = True``.
- ``ci_cd`` has no real dependency to verify yet — ``runners/main/deploy.py`` is a no-op stub (``def run(self): pass``). Implementing a real deploy flow (and the dependency it needs) is the actual work here.
- ``data_analysis`` has its ``pyproject.toml`` fragment in place (``pandas``/``numpy``/``matplotlib``/``seaborn``/``scikit-learn``), but its own code is the bigger piece of work: ``domain/models/data_analysis.py`` doesn't use any of them yet — it's a hand-rolled, illustrative sketch over plain ``list[dict]`` records. The intended direction is real, DataFrame-backed tooling: reading and writing Excel and JSON, cleaning and summarizing data with pandas, in place of the placeholder classes there now.
- ``data_visualization`` ships no dependency file at all yet, and its ``Chart``/``BarChart``/``LineChart``/``PieChart`` classes only ``print()`` what they would plot — no charting library is wired in. The intended direction is real chart generation with matplotlib, in place of those placeholders, with a ``pyproject.toml`` fragment declaring it as a main dependency once that code exists.

**Build a stub template from scratch.** These exist only as a name, a description and an aspirational dependency list, with no real scaffolding yet — a green-field case for `Creating New Templates`_:

- ``graphql``, ``rabbitmq`` — no files beyond the template class itself.
- ``machine_learning``, ``websockets`` — a ``pyproject.toml`` fragment already lists the expected dependencies (``scikit-learn``/``tensorflow``/``keras``/... for the former, ``websockets``/``python-socketio``/``aiohttp``/``websocket-client`` for the latter), but no actual code beyond ``__init__.py`` yet.
- ``tests`` — same shape (a ``pyproject.toml`` fragment with ``pytest``/``coverage``/... already declared, no real scaffold). Worth opening an issue to confirm scope before starting: Appcraft scaffolds *generated* projects, and has no automated test suite of its own, so a "tests template" means testing setup for the project it's installed into, a narrower goal than the name suggests.

**Bring in a framework that isn't represented yet.** There's no ``TemplateABC`` subclass for this one at all yet, so it starts from scratch in `Creating New Templates`_:

- **FastAPI**, as an alternative to ``flask`` for a project's web layer. The :doc:`Flask Template family <../templates/flask/index>`'s shape is the natural precedent: a shared, non-standalone base owning the app factory and router, with ``flask_api``/``flask_ui``-style siblings whose routes are auto-discovered rather than registered by hand — adapted to FastAPI's own routing and dependency-injection style.

**Add a sibling adapter to an existing family.** The interchangeable-adapters pattern (see :doc:`../architecture/index`) is built for this — a ``gitlab`` or ``bitbucket`` template, for instance, needs no change to ``remote_repository`` itself, only a concrete adapter and ``is_installed()`` wiring, with ``github`` as the model to follow. Same idea for another database or web-scraping engine.

**Strengthen the project's own testing and CI.** Appcraft has no automated test suite for itself, and CI only accumulates a release's already-built docs into the ``docs`` branch and publishes them — it doesn't run ``sphinx-build``, ``pyright``, or any lint/type check on a pull request. Both apply to the whole repository, not to one template.

Creating New Templates
----------------------

To create a new template, follow these steps:

1️⃣ **Clone the repository and install it in editable mode**:
    .. code-block:: bash

        git clone https://github.com/duxtec/appcraft.git
        cd appcraft
        pip install -e .

2️⃣ **Run the template creator**:
    .. code-block:: bash

        python -m appcraft.utils.template.creator <template_name>

    This generates ``appcraft/templates/<template_name>/`` with a starter ``__init__.py``, a ``files/pyproject.toml`` stub, and one-file ``runners/main`` and ``runners/tools`` runners — ready to build on.

3️⃣ **Edit the generated ``__init__.py``**:
    - Write a real ``description``.
    - Set ``dependencies``, ``standalone``, ``exclusive_group``, ``pre_install``/``post_install`` as needed.
    - Set ``active = True`` once the template is ready — templates default to ``active = False`` (hidden from ``list_templates``/``init``/``add_template`` unless ``--install-inactive`` is passed) until you do.

4️⃣ **Develop the template's files using a temporary project** — see `Working in a Temporary Project`_ below. Editing files directly under ``appcraft/templates/<template_name>/files/`` is not supported: dependencies on other templates, IDE/linter resolution, and the framework's own runtime utilities are only correctly wired up inside a real generated project.

5️⃣ **Submit a pull request with the new template**.

Updating Existing Templates
-----------------------------

Updating an existing template follows the same loop as creating one — jump straight to `Working in a Temporary Project`_, skipping template creation.

Translating the Framework
--------------------------

Translations aren't per-template — they're centralized in the ``locales`` template, which ships gettext catalogs at ``appcraft/templates/locales/files/locale/<lang>/LC_MESSAGES/<domain>.po`` (plus a compiled ``.mo`` next to each), where ``<domain>`` groups related strings (e.g. ``app``, ``core``, ``database``). Existing languages are ``en`` and ``pt_BR``.

To add a language:

1️⃣ **Copy an existing language folder** under ``locale/`` and rename it to the new locale code (e.g. ``es`` for Spanish).

2️⃣ **Translate each ``.po`` file's msgid/msgstr pairs**, keeping the file structure and domain names unchanged.

3️⃣ **Recompile to ``.mo``** (the ``locales`` template's own runtime also does this automatically for any ``.po`` newer than its ``.mo``, but compiling ahead of time catches syntax errors early):
    .. code-block:: bash

        msgfmt locale/<lang>/LC_MESSAGES/<domain>.po -o locale/<lang>/LC_MESSAGES/<domain>.mo

4️⃣ **Test it** in a temporary project with the ``locales`` template installed — see `Working in a Temporary Project`_ — by setting ``lang`` in ``config/app.toml`` to the new code.

5️⃣ **Submit a pull request with the new language**.

Working in a Temporary Project
-------------------------------

Every template — new or existing — is developed inside ``appcraft/templates/temp/files``, a disposable sandbox project, never by editing a template's own ``files/`` directly.

1. **From the appcraft repo root**, run:
    .. code-block:: bash

        python -m appcraft.cli init <template_names...>

    Running ``init`` from the repo root (or from inside ``appcraft/templates/temp/files`` itself) is what triggers the sandbox behavior: it wipes ``appcraft/templates/temp/files``, recreates it, and installs the requested templates there instead of into the current directory — so it becomes a real, runnable generated project containing exactly those templates.

2. **Edit, add, or remove files inside ``appcraft/templates/temp/files``** as you would in any generated project — run its runners, add dependencies, and so on — to develop or fix a template's behavior.

3. **Save your changes back to the real template**:
    .. code-block:: bash

        appcraft save_template <template_name>

    This reads ``temp/files``'s own installed-templates registry to tell which files belong to ``<template_name>`` versus any other templates also installed in ``temp``, then copies every new/changed file back into ``appcraft/templates/<template_name>/files/`` and deletes files there that no longer exist in ``temp/files``.

    **Modify only one template at a time.** If you need to work on another template next, save the current one first, then repeat from step 1 — ``temp/files`` is wiped on every ``init`` run from the repo root, so nothing is preserved there between sessions.

4. **Submit a pull request** once the change is saved to the real template directory.

Ready to Contribute?
--------------------

If you have any questions, feel free to open an issue or reach out to the maintainers.

🚀 Happy Coding!
