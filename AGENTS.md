# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, GitHub Copilot, Windsurf, and others that read `AGENTS.md`) when working with code in this repository.

## Project Overview

Appcraft is a Python CLI tool that scaffolds and extends Python projects built on a Clean Architecture layout (domain / application / infrastructure / presentation / runners). Functionality is added to a generated project by installing composable **templates** (`appcraft init <template_names>`), each of which drops a set of files into the target project and can declare dependencies on other templates.

There is no automated test suite in this repository.

## Commit conventions

Never add a `Co-Authored-By: Claude` (or similar) trailer to commit messages in this repository.

## Development Commands

```bash
# Install in editable mode (registers the `appcraft` console script via pyproject.toml)
pip install -e .

# Run the CLI directly from source without installing
python -m appcraft.cli init <template_names...>
python -m appcraft.cli add_template <template_names...>  # add templates to an existing project
python -m appcraft.cli list_templates
python -m appcraft.cli save_template <template_name>

# Type checking (strict mode; scope is set in pyrightconfig.json)
pyright

# Build the Sphinx docs (source lives in appcraft/docs/latest, output is published
# from appcraft/docs/build/latest for GitHub Pages via .github/workflows/static.yml)
cd appcraft/docs/latest && make html
```

Because `appcraft/utils/__init__.py` imports helpers (`Printer`, `ImportManager`, `PackageManager`, `PoetryManager`, `PipenvManager`) directly from `appcraft/templates/base/files/infrastructure/framework/appcraft/...`, the CLI package cannot run without the `base` template's files present — they are the CLI's own runtime utilities, not just scaffold output.

## Detailed reference

This repo contains two things layered on top of each other: the **appcraft CLI/template engine**, and the **generated-project framework** that the CLI's `base` template installs into user projects — including the naming/layering conventions every active template follows (`git`/`github` are deliberately `active = False` for not following them yet — see `docs/agents/templates-git.md`). Start with `docs/agents/architecture.md`.

Per-template-family details — file layout, the specific `is_installed()`-based extension points each family uses, and anything non-obvious about how they work — live in their own files so this index stays short:

@docs/agents/architecture.md
@docs/agents/templates-database.md
@docs/agents/templates-flask.md
@docs/agents/templates-web-scraping.md
@docs/agents/templates-package-managers.md
@docs/agents/templates-git.md
@docs/agents/templates-misc.md
