# Everything else

Templates that don't belong to a documented family above, grouped by actual readiness (verified against `active`/file counts as of 2026-09-22 — re-check before relying on this if it's been a while, `active` in each `__init__.py` and `find appcraft/templates/<name>/files -type f | wc -l` are both cheap to re-verify). `docker` gets its own paragraph below rather than a family file — it has no sibling templates, but it's substantial enough (dynamic compose generation, prod/dev split) not to lump in with the stubs.

## Active, standalone utility templates

No sibling family, no shared base — each is a self-contained addition.

- **`prompt_toolkit`** — adds the `prompt-toolkit` dependency that powers the runner system's interactive module/class/method menu (see [architecture.md](architecture.md#the-runner-system)). The runner system works without it as long as the full path is always passed on the command line; without this template, only that inline-args mode is available.
- **`docker`** — containerizes the app: a single Dockerfile (installs through whichever of poetry/pipenv/uv is active, non-root user, skips dev-only deps in production), and a `docker-compose.yml` generated automatically from every `runners/main` `Runner` exposing a `start` action — one service per deployable entry point, discovered the same way the web_scraping benchmark tool discovers runners (see [templates-web-scraping.md](templates-web-scraping.md)). `python run_tools docker {build,up,down,generate_compose}` wraps `docker compose` (falling back to the standalone `docker-compose` v1 binary) so none of that needs `cd infrastructure/docker` first. Flask's own runner is environment-aware (`config/app.toml`'s `environment = "production"` switches it from the Werkzeug dev server to gunicorn) specifically so this template's production path means something.

## `active = False`, real content, never finished/activated

These have actual scaffolding (not stubs) but are hidden from `list_templates`/`init` until someone verifies them and flips `active = True`. Don't assume they're production-ready just because files exist.

- **`git`** / **`github`** — fully functional, but deliberately deactivated: still on the pre-`Port`/`use_cases` architecture. See [templates-git.md](templates-git.md) for what exactly is stale and what re-activating them requires.
- **`locales`** / **`logs`** — deliberately deactivated (2026-09-23): both ship a `Pipfile` declaring real dependencies (`polib`; `structlog`/`rich`/`better-exceptions`/`logbook`/`flask-logging`/`graypy`) but no `pyproject.toml` equivalent. `TemplateAdder._copy_directory_contents` only copies a `Pipfile` for Pipenv-based projects (`os.path.basename(s) in ("Pipfile", "Pipfile.lock") and not isinstance(self.package_manager, PipenvManager)` skips it otherwise), so for the default (Poetry) a project, these dependencies are never actually installed via the normal path — the framework's own runtime auto-install (`ErrorHandler.handle_import_error`, see [architecture.md](architecture.md)) silently papers over this the first time the missing import is hit, but that's a fragile safety net, not a fix. Re-activate once each gets a `pyproject.toml` fragment declaring its real dependencies as main deps (matching how `flask`'s and `base`'s own missing-dependency bugs were fixed this session). Their `is_installed()` is checked at runtime by `Initializer.execute_runner()`/`ComponentPrinter` to conditionally enable locale-aware behavior when re-activated (see [architecture.md](architecture.md)'s `project_init` bullet for how that's wired) — that wiring itself is unaffected by this bug.
- **`ci_cd`** (11 files) — CI/CD pipeline scaffolding, includes a `runners/main/deploy.py` and Sphinx docs config. Same `Pipfile`-only dependency gap as `locales`/`logs`.
- **`data_analysis`** (9 files) — includes a `domain/models/data_analysis.py` and Sphinx docs config. Same `Pipfile`-only dependency gap as `locales`/`logs`.
- **`data_visualization`** (8 files) — includes a `domain/models/charts.py` and Sphinx docs config.

Check each one's actual layer usage before treating it as a naming-convention reference — it hasn't been confirmed to follow the [current conventions](architecture.md#naming-and-layering-conventions) the way the active templates have (`git`/`github` are the one case here where this *has* been checked — and confirmed stale, see above).

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
