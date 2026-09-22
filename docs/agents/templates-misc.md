# Everything else

Templates that don't belong to a documented family above, grouped by actual readiness (verified against `active`/file counts as of 2026-09-21 — re-check before relying on this if it's been a while, `active` in each `__init__.py` and `find appcraft/templates/<name>/files -type f | wc -l` are both cheap to re-verify).

## Active, standalone utility templates

No sibling family, no shared base — each is a self-contained addition.

- **`locales`** — localization file structure. Its `is_installed()` is checked at runtime by `Initializer.execute_runner()`/`ComponentPrinter` to conditionally enable locale-aware behavior (see [architecture.md](architecture.md)'s `project_init` bullet for how that's wired).
- **`logs`** — logging configuration (rotation, levels, outputs). Same `is_installed()` runtime-detection wiring as `locales`.
- **`prompt_toolkit`** — adds the `prompt-toolkit` dependency that powers the runner system's interactive module/class/method menu (see [architecture.md](architecture.md#the-runner-system)). The runner system works without it as long as the full path is always passed on the command line; without this template, only that inline-args mode is available.

## `active = False`, real content, never finished/activated

These have actual scaffolding (not stubs) but are hidden from `list_templates`/`init` until someone verifies them and flips `active = True`. Don't assume they're production-ready just because files exist.

- **`ci_cd`** (11 files) — CI/CD pipeline scaffolding, includes a `runners/main/deploy.py` and Sphinx docs config.
- **`data_analysis`** (9 files) — includes a `domain/models/data_analysis.py` and Sphinx docs config.
- **`data_visualization`** (8 files) — includes a `domain/models/charts.py` and Sphinx docs config.
- **`docker`** (4 files) — includes a `runners/main/docker.py`.

Check each one's actual layer usage before treating it as a naming-convention reference — it hasn't been confirmed to follow the [current conventions](architecture.md#naming-and-layering-conventions) the way the active templates have.

## Pure stubs — description only, no scaffold at all

`TemplateABC` subclass exists (so they can be referenced/discussed), but `files/` is empty or near-empty. These are ideas on the roadmap, not started:

- **`graphql`** (0 files)
- **`rabbitmq`** (0 files)
- **`machine_learning`** (1 file — just `__init__.py`)
- **`websockets`** (1 file — just `__init__.py`)
- **`tests`** (1 file — just `__init__.py`) — worth a second look before ever building this one out: the project itself has [no automated test suite](../../AGENTS.md), so a "tests template" that scaffolds testing setup for *generated* projects is a different, narrower scope than it might sound like — confirm intent before starting.

## Framework-level quality gaps (not a specific template)

- No automated test suite for `appcraft` itself (confirmed in the root `AGENTS.md`) — `TemplateLoader.resolve()`, `install()`/`uninstall()`, `TemplateSaver`, etc. have zero test coverage despite `pyright --strict` being enforced.
- CI (`.github/workflows/static.yml`) only builds and publishes the Sphinx docs — it does not run `pyright` or any lint/type-check on push/PR. All such verification today is manual (`pyright` from the repo root).
