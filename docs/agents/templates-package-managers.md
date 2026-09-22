# Package manager templates (`poetry`, `pipenv`, `uv`)

All three share `exclusive_group = "package_manager"` (see the `TemplateABC` attribute reference in [architecture.md](architecture.md)) — `TemplateLoader.resolve()` rejects requesting two of them *together* in one `init`/`add_template` call (`TemplateConflictError`). Installing one when a different one is already present is a deliberate swap: `TemplateABC.install()` automatically calls the currently-installed sibling's `.uninstall()` first (generic `exclusive_group` behavior, not specific to package managers — see [architecture.md](architecture.md)), and each template's own `pre_install` converts whatever dependency state that leaves behind into its own format. None of the three depends on another — swapping in either direction works the same way.

## Where the manifest actually lives

`base` ships the project's *only* `pyproject.toml` (`base/files/pyproject.toml` — real baseline deps `toml`/`pydantic`, dev deps `sphinx`/`flake8`/`black`/`isort`, and project metadata/`[build-system]`), not `poetry`. `poetry`/`pipenv`/`uv` never ship a full manifest of their own — each only ships a small fragment declaring `appcraft` as a dev dependency (for `pre_install`'s own import, see below) merged in via `TemplateAdder.merge_pm_files`. This is why none of the three needs to depend on another to guarantee something exists to read from: `base` is unconditionally installed before any package-manager template's `pre_install` runs (its own `install()` file-copy happens in an earlier phase — see the install-order note in [architecture.md](architecture.md)).

## `poetry` (active, `default = True`)

Included in every `init` automatically (`default = True`), whether or not it's named explicitly. Owns just `.vscode/settings.json` (points the `ms-python.python` extension at Poetry) — that's the only file removed if you swap away from it.

## `pipenv` (active)

## `uv` (active)

All three (including `poetry`) switch dependency management to their own format by reading whatever currently exists and rewriting it — fully symmetric, so swapping in any direction (poetry → pipenv → uv → poetry → ...) round-trips the same dependencies, groups, and metadata each time:

- `pre_install(cls, target_dir)` calls `appcraft.utils.dependency_convert.read_dependencies(target_dir)` to snapshot current dependencies (main + grouped dev deps + Python version + project metadata) regardless of source format (Poetry-, uv-, or Pipfile-style — whichever is currently in `pyproject.toml`/`Pipfile`), then writes that snapshot out in its own target format:
  - `pipenv` → a `Pipfile` (`toml.dump`).
  - `uv` → native PEP 621 `[project]`/`[dependency-groups]` tables in `pyproject.toml`.
  - `poetry` → `[tool.poetry.*]` tables in `pyproject.toml`.

  Each then calls `clear_dependency_sources(target_dir)` (removes `Pipfile`/`Pipfile.lock`, strips whichever dependency tables were previously there — from `pyproject.toml` or `Pipfile` — while preserving project metadata and `[build-system]`) and `set_package_manager_config(target_dir, "pipenv" | "uv" | "poetry")`.
- This runs in the **pre-install** phase — before `PackageManagerBase()` installs requirements — specifically so that class picks the *newly*-configured manager, not the old one (see the install-order note in [architecture.md](architecture.md)).
- **`appcraft.utils.dependency_convert` import must stay local to `pre_install`, not at module level.** This `__init__.py` is copied into every generated project as the `is_installed()` marker (`infrastructure/framework/appcraft/templates/<name>/__init__.py` — see [architecture.md](architecture.md)'s `project_init` bullet), but `appcraft.utils.dependency_convert` lives in the CLI package, which only exists in the dev environment — never inside a generated project. A module-level import would crash every generated project's marker file on any `is_installed()` check. All three templates declare `appcraft` as a **dev** dependency (in their own `pyproject.toml` fragment merged in by `TemplateAdder`) purely so pyright can resolve the import when editing appcraft's own source, with `# pyright: ignore[reportMissingImports]` since it still won't resolve inside an actual generated project that hasn't installed `appcraft` itself.

## Swap mechanics (`exclusive_group` + `uninstall()`)

`TemplateABC.install()` checks `cls.exclusive_group`: if set, it looks up every currently-installed template (via `TemplateManager`) sharing that same group and calls each one's `.uninstall()` before proceeding — generic engine behavior, documented in [architecture.md](architecture.md), not package-manager-specific code. `TemplateABC.uninstall()` (previously a no-op) now deletes whichever files `TemplateManager` recorded as that template's own (skipping any also owned by another still-installed template) and removes its `templates.json` entry — so `is_installed()` correctly flips after a swap, and per-template leftover files (like `poetry`'s `.vscode/settings.json`) don't linger. It does **not** duplicate the `Pipfile`/dependency-table cleanup — that's already handled unconditionally by the *newly*-installing manager's own `pre_install` → `clear_dependency_sources()` call above, regardless of which manager was active before.

Verified end-to-end (2026-09-21): `init` (poetry) → `add_template pipenv` → `add_template uv` → `add_template poetry` round-trips the same dependencies/metadata at every step, correctly removes/restores `.vscode/settings.json`, and `add_template pipenv uv` (two members of the group at once) raises `TemplateConflictError` as expected.
