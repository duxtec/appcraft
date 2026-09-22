# Git templates (`git`, `github`)

## ⚠️ `active = False` — temporarily deactivated, not yet migrated

Unlike every other template in this repo, `git` and `github` still use the **older** convention that predates the `Port`/`use_cases` refactor described in [architecture.md](architecture.md#naming-and-layering-conventions):

- `application/services/` instead of `application/use_cases/` (e.g. `application/services/github.py`'s `GitHubRepositoryService`).
- `AdapterInterface` suffix instead of `Port` (`application/services/interfaces.py`'s `ServiceAdapterInterface`, `application/interfaces/adapters.py`'s `AdapterInterface`) — the exact anti-pattern flagged and corrected for `web_scraping` (see [templates-web-scraping.md](templates-web-scraping.md)).

Since this is the only place `AdapterInterface`/`application/services/` still appear, both were set `active = False` (hidden from `list_templates`/`init`/`add_template` unless `--install-inactive`) rather than left active with known-bad code as the only example someone building a new template might copy. Treat migrating `git`/`github` to `application/use_cases/` + `Port` as the condition for re-activating them, not a stylistic nice-to-have — do not use either as a naming/layering reference in the meantime.

## `git`

Ships `.gitignore` and a default repository structure. `post_install(cls, target_dir)` runs `subprocess.check_call(["python", "run_tools", "git", "init"])` — invoking the *generated app's own* `git` runner (`runners/tools/git.py`) rather than shelling out to `git init` directly, so it reuses whatever the runner already does (error handling via `Printer`, consistent with the rest of the generated project).

## `github` (`dependencies = ["git"]`)

Adds GitHub-specific tooling (`infrastructure/github/adapter.py` wrapping the `gh` CLI, `runners/tools/github.py`, `presentation/cli/github.py`).
