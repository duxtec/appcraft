Git Template
=============================

The **Git Template** sets up a local Git repository for a generated project and gives it the tooling to work with it: a configurable branching strategy, Conventional Commits, automatic next-version detection, and stage-based releases. It doesn't need a hosting platform — install the `GitHub Template <../github/index.html>`_ (or a future platform template) to publish the repository.

It's **standalone**, so ``appcraft init git`` works on its own.

What it sets up
-----------------

- A local repository with the branches your branching strategy defines (see below), created from the first commit.
- A ``commit-msg`` git hook that blocks breaking changes from landing directly on major-version branches (see `Breaking changes`_).
- ``.gitignore`` and ``config/git.toml``, which describes the branching strategy.

Setting up the branching strategy
------------------------------------

The first ``python tools git init`` creates the branches. If the strategy hasn't been chosen yet (``configured = false`` in ``config/git.toml``), it asks, in a terminal, whether to use major-version branches, the current major version, and the stages. Press Enter to keep each default.

The answers can also come as arguments, which skips the questions and is what automation uses:

.. code-block:: bash

    python tools git init use_major_version=true major_version=2 stages=alpha,beta,main
    python tools git init use_major_version=false stages=none trunk_branch=main

With ``interactive=false``, ``init`` never asks: without arguments it uses the values in ``config/git.toml``. Once the strategy is set up, ``init`` refuses arguments: change ``config/git.toml`` by hand and create the branches you need.

Branching strategy (``config/git.toml``)
------------------------------------------

Everything about branches is driven by one file:

.. code-block:: toml

    use_major_version = false   # branch names get a "v{N}-" prefix when true
    major_version = 0           # current major line; only read when use_major_version = true
    stages = ["alpha", "beta", "main"]   # ordered, least- to most-stable; empty = no stage concept
    trunk_branch = "main"       # only used when stages = [] (single-branch case)

``use_major_version`` and ``stages`` are independent, which gives four layouts:

.. list-table::
    :header-rows: 1

    * - Layout
      - Config
      - Branches created
    * - Major version and stages
      - ``use_major_version = true``, ``stages = [...]``
      - ``v0-alpha``, ``v0-beta``, ``v0-main``
    * - Major version only
      - ``use_major_version = true``, ``stages = []``
      - ``v0``
    * - Stages only
      - ``use_major_version = false``, ``stages = [...]``
      - ``alpha``, ``beta``, ``main``
    * - Single branch
      - ``use_major_version = false``, ``stages = []``
      - ``main`` (from ``trunk_branch``)

The most stable branch — the last stage, or the single branch when there are no stages — is the **base branch**. Feature and fix branches are always created from it.

Feature and fix branches
---------------------------

Work happens on short-lived branches named ``<type>/<name>``, created from the base branch. The type is any Conventional Commits type, so the branch name says what kind of change it holds:

.. code-block:: bash

    python tools git start feat login-page
    python tools git start fix null-pointer
    python tools git start refactor parser

Branch types don't change the version by themselves; the commit types do.

Each change is merged into a stage on its own. Once validated, the **same** branch is merged into the next stage — there's never a direct merge from ``beta`` into ``main``:

.. code-block:: bash

    python tools git merge feat/login-page beta   # test it on beta
    python tools git merge feat/login-page main   # promote it once validated

A stage branch that doesn't exist yet is created the first time something is merged into it, from the stage just before it. For example, the first merge into ``v1-beta`` creates it from ``v1-alpha``. The command says so when it happens.

Conventional Commits
-----------------------

Commit messages follow `Conventional Commits <https://www.conventionalcommits.org/>`_. The type decides how the next version is computed:

- ``feat:`` — a new feature (minor bump).
- ``fix:`` and ``perf:`` — a fix or performance change (patch bump).
- ``feat!:``, ``fix!:``, or a ``BREAKING CHANGE:`` footer — a breaking change. It bumps the major version, except while the version is ``0.x``: then it bumps the minor, following semver. ``1.0.0`` comes from cutting a new major line once the current one has a stable release.
- ``docs:``, ``chore:``, ``refactor:``, ``test:``, ``style:``, ``build:``, ``ci:``, ``revert:`` — don't change the version on their own.

Breaking changes
-------------------

When ``use_major_version = true``, a breaking change is treated according to the state of the current major line:

- If the line has **no stable release yet**, or has only pre-releases, a breaking change is merged like any other change. Nothing is redirected.
- If the line **has a stable release** (for example ``0.1.0`` on ``v0``), a breaking change can't land on it. It has to go into the next major line.

This is enforced in two places:

- **Merging** with ``python tools git merge <source> <target>`` checks the incoming commits. If one is breaking and the line has a stable release, the merge is redirected to a new ``v{N+1}-alpha`` branch, created from the current base branch, and the target isn't touched. Only the entry stage (``alpha``) is created: the new major line starts unproven and is promoted like anything else.
- **Committing or merging directly** with ``git commit``/``git merge`` is blocked by the ``commit-msg`` hook when the current branch is a major-version branch, the commit is breaking, and the line has a stable release. The hook doesn't redirect anything; it tells you to make the change on a feature branch and merge it with the command above.

With ``use_major_version = false`` there's no major line to protect, and breaking changes are allowed everywhere.

Pausing at the end of a command
-----------------------------------

``detect_version`` and ``changelog`` wait for a keypress at the end when they run in a terminal, so their output stays on screen. Pass ``pause=false`` to skip the pause, for example in scripts:

.. code-block:: bash

    python tools git detect_version pause=false

Releases
-----------

Releases are cut with one command, run from a stage branch:

.. code-block:: bash

    python tools git release

It reads the commits that no tag contains yet, computes the next version for the current stage, shows it and asks for confirmation. Pass ``interactive=false`` to publish without the question, as in a script. On confirmation it writes the version to ``pyproject.toml``, commits ``chore(release): vX.Y.Z``, creates the tag and — if the GitHub template is installed and the repository has a remote — publishes a GitHub release too. ``python tools git detect_version`` shows what the release would be without changing anything.

The stage of the branch decides what kind of release it is:

.. list-table::
    :header-rows: 1

    * - Branch
      - Release
      - Example
    * - ``alpha``
      - Pre-release ``a``, counted per version
      - ``0.7.0a1``, ``0.7.0a2``
    * - ``beta``
      - Pre-release ``b``, counted per version
      - ``0.7.0b1``
    * - Base branch (``main``, or ``v{N}`` with major versions only)
      - Stable
      - ``0.7.0``

The base is the highest release of the line across **every** stage, so a release from ``main`` sees the releases made on ``alpha`` and ``beta``, whatever branch they were cut from. The next version then follows these rules:

- **A major line without stages** is a single branch (``v0``), and all of its releases are stable: the first is ``0.0.0``, then the usual SemVer bumps.
- **After a pre-release** ``X``, a ``fix:`` stays in the same version: ``0.6.0a1`` → ``0.6.0a2``. A ``feat:`` or a breaking change opens the next one: ``0.6.0a2`` → ``0.7.0a1``. Promoting the same commits to a later stage keeps the version: ``0.8.0a1`` → ``0.8.0b1`` → ``0.8.0``.
- **After a stable release**, the usual SemVer bump applies: ``0.8.0`` → ``0.8.1a1`` (fix), ``0.9.0a1`` (feat), ``1.0.0a1`` (breaking).
- **A breaking change is a minor bump only while there are no releases at all**. Once any release exists, it's a major bump.
- Each pre-release label counts on its own: a second alpha of ``0.6.0`` is ``0.6.0a2``.
- A version can stop at any stage: ``0.6.0a1`` with no beta and no stable is perfectly valid.

The version is written in PEP 440 format, which pip and poetry understand; ``pip install`` skips pre-releases unless you pass ``--pre``.

Releases can only be cut from a stage branch of the current major line. Running ``release`` from a feature branch is refused.

When a **stable** release of a higher major version is cut, the repository's default branch on the platform moves to that major's base branch. After ``1.0.0`` is released from ``v1-main``, GitHub's default branch becomes ``v1-main``. Pre-releases never change it.

The project's version lives in one place, ``pyproject.toml`` (``[project]`` or ``[tool.poetry]``). The application reads it at runtime, so there's no second copy to keep in sync. Edits to ``pyproject.toml`` and ``config/git.toml`` only touch the value that changes, so comments in those files are kept.

Cutting a major version on purpose
-------------------------------------

A new major line is normally cut automatically when a breaking change is merged into a major-version branch. To cut it explicitly, without a breaking commit, run this (requires ``use_major_version = true``). The new major is always the one right above the **highest** existing major, whichever branch you're on:

.. code-block:: bash

    python tools git new_major

It creates the entry stage of the next line (``v1-alpha``) from the base branch, bumps ``major_version`` on that branch, and switches to it. Running it again is safe: it doesn't create or bump anything twice.

A new major line only starts once the highest major has shipped a stable release (for example ``1.0.0`` on ``v1``). Before that, ``new_major`` is refused, and no major is created above it. Breaking changes merged into the highest major are accepted until then.

A breaking change only goes to a new major when the highest major is the one it's merged into. If a major above the target already exists, the merge is refused with an alert, whether the target is the highest major or not.

Changelog
------------

``python tools git changelog`` prints the commits that the next release would contain (the ones no tag contains yet), grouped into breaking changes, features, fixes, performance and other changes. Release commits and merge commits are left out.

``python tools git changelog output=CHANGELOG.md`` also writes that section to the top of the file, above anything already there.

Cleaning up merged branches
------------------------------

``python tools git cleanup`` lists the feature and fix branches already merged into the base branch, both locally and on ``origin``, asks for confirmation, and deletes them from both places. Branches that aren't merged are never touched. The remote is refreshed with a fetch first, so the list reflects what's on the server.

Remote repository
--------------------

``python tools git set_remote <url>`` points ``origin`` at an existing repository and pushes every branch. To create the repository on a hosting platform instead, install a platform template such as the `GitHub Template <../github/index.html>`_ and use the `Remote Repository Template <../remote_repository/index.html>`_ commands.

Limitations
--------------

- A squash merge leaves only the squashed message in history, so the individual commit types are lost for version detection. Prefer regular merges.
- ``python tools git init`` also works on a repository that already exists: it keeps the existing history and only creates the configured branches that are missing. Existing branches are never renamed. Run it once to get the ``commit-msg`` hook installed.
- ``git commit --no-verify`` skips the hook, as in any git repository.
