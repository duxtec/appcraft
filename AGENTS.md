# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, GitHub Copilot, Windsurf, and others that read `AGENTS.md`) when working with code in this repository.

## Project Overview

Appcraft is a Python CLI tool that scaffolds and extends Python projects built on a Clean Architecture layout (domain / application / infrastructure / presentation / runners). Functionality is added to a generated project by installing composable **templates** (`appcraft init <template_names>`), each of which drops a set of files into the target project and can declare dependencies on other templates.

There is no automated test suite in this repository.

## Commit conventions

Never add a `Co-Authored-By: Claude` (or similar) trailer to commit messages in this repository.

## Documentation conventions

Every template's documentation page must describe **all** of its runners: the main ones shown as examples, and the auxiliary ones used for configuration or any other maintenance task (setup, cleanup, inspection, changelog, and so on). A runner missing from the docs counts as undocumented. Keep the agent docs (`docs/agents/`) and the user docs (`docs/<version>/source/templates/`) in step when a runner changes.

## Runner conventions

Runs are interactive by default: a question is asked whenever a value is missing. `interactive=false` turns questions off, for scripts and CI. With it, a missing or invalid argument is an error that names the argument and exits with status 1, and a confirmation takes its default (a publish or a deletion of branches proceeds). Never add a per-question argument for a confirmation. Use `read_input` from `infrastructure/core/runner/mode.py` for any question, so the rule holds everywhere.

## Typing conventions

Prefer an `Enum` (`class X(str, Enum)`) over `typing.Literal` whenever a value is limited to a fixed set of options, including CLI/runner parameters. Use the enum type in signatures and validate input against its members (e.g. `ConventionalCommitType` in `domain/git/commit.py`). Existing `Literal` usages stay as they are unless the task touches them.

## Development Commands

```bash
# Install in editable mode (registers the `appcraft` console script via pyproject.toml)
pip install -e .

# Run the CLI directly from source without installing (`appc` is an alias of `appcraft`)
python -m appcraft.cli init <template_names...>
python -m appcraft.cli add_template <template_names...>  # add templates to an existing project
python -m appcraft.cli list_templates
python -m appcraft.cli save_template <template_name>

# Type checking (strict mode; scope is set in pyrightconfig.json)
pyright

# Build the Sphinx docs of a version folder (source lives in docs/<version>/source;
# the built output is committed under docs/build/<version> and published by the
# docs.yml workflow on release — it doesn't run sphinx-build itself)
sphinx-build -b html docs/<version>/source docs/build/<version>
```

Because `appcraft/utils/__init__.py` imports helpers (`Printer`, `ImportManager`, `PackageManager`, `PoetryManager`, `PipenvManager`) directly from `appcraft/templates/base/files/infrastructure/framework/appcraft/...`, the CLI package cannot run without the `base` template's files present — they are the CLI's own runtime utilities, not just scaffold output.

`pyrightconfig.json` includes `appcraft/templates` wholesale, so pyright reports an unresolved import for anything a template imports that isn't actually installed in *this* repo's own dev environment — Flask, SQLAlchemy, pandas, and so on are scaffold content the CLI ships, never a real dependency of the CLI itself, so the root `pyproject.toml` doesn't declare them (not even as an optional group — a group that existed here briefly for exactly this purpose was removed: those packages belong only in a generated project's own manifest, never in the framework's). This noise is expected and not a bug to chase: the correct way to verify a template's own code is the `appcraft/templates/temp/files` dev loop (see below), which installs that template's real dependencies into its own, separate venv.

## Detailed reference

This repo contains two things layered on top of each other: the **appcraft CLI/template engine**, and the **generated-project framework** that the CLI's `base` template installs into user projects — including the naming/layering conventions every active template follows. Start with `docs/agents/architecture.md`.

Per-template-family details — file layout, the specific `is_installed()`-based extension points each family uses, and anything non-obvious about how they work — live in their own files so this index stays short:

@docs/agents/architecture.md
@docs/agents/templates-database.md
@docs/agents/templates-flask.md
@docs/agents/templates-web-scraping.md
@docs/agents/templates-package-managers.md
@docs/agents/templates-git.md
@docs/agents/templates-misc.md
