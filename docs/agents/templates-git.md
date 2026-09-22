# Git templates (`git`, `github`)

## `git` (active)

Ships `.gitignore` and a default repository structure. `post_install(cls, target_dir)` runs `subprocess.check_call(["python", "run_tools", "git", "init"])` — invoking the *generated app's own* `git` runner (`runners/tools/git.py`) rather than shelling out to `git init` directly, so it reuses whatever the runner already does (error handling via `Printer`, consistent with the rest of the generated project).

## `github` (active, `dependencies = ["git"]`)

Adds GitHub-specific tooling (`infrastructure/github/adapter.py` wrapping the `gh` CLI, `runners/tools/github.py`, `presentation/cli/github.py`).

## ⚠️ Known technical debt: not yet migrated to the current architecture

Unlike every other active template, `git` and `github` still use the **older** convention that predates the `Port`/`use_cases` refactor described in [architecture.md](architecture.md#naming-and-layering-conventions):

- `application/services/` instead of `application/use_cases/` (e.g. `application/services/github.py`'s `GitHubRepositoryService`).
- `AdapterInterface` suffix instead of `Port` (`application/services/interfaces.py`'s `ServiceAdapterInterface`, `application/interfaces/adapters.py`'s `AdapterInterface`) — the exact anti-pattern flagged and corrected for `web_scraping` (see [templates-web-scraping.md](templates-web-scraping.md)).

This is the only place in the active template set where `AdapterInterface`/`application/services/` still appear — do not use either as a reference when building a new template, and treat migrating `git`/`github` to `application/use_cases/` + `Port` as open work, not a stylistic choice.
