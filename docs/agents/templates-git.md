# Git templates (`git`, `remote_repository`, `github`)

`git`/`github` used to be the only templates left on the pre-`Port`/
`use_cases` architecture (`application/services/`, `AdapterInterface`) and
were deliberately `active = False` for it. Both are now migrated and active,
and GitHub hosting support is split out as a third template,
`remote_repository`, following the same
[interchangeable-sibling-adapters-via-`is_installed()`](architecture.md#the-interchangeable-sibling-adapters-via-is_installed-pattern)
pattern as `sqlalchemy`/`mongodb` and `selenium`/`playwright`/`httpx`/
`curl_cffi`: a shared, non-`standalone` base owns the `Port` + generic
runner + `Provider`, and `github` contributes only a concrete `Adapter`.
`gitlab`/`bitbucket`-style siblings can be added later with zero changes to
`remote_repository` itself.

## `git` (active, standalone)

Local git operations, a configurable branching strategy, Conventional
Commits parsing, and automatic next-version detection — no knowledge of any
hosting platform at all.

- `application/ports/git.py` — `GitPort`: `is_repository`, `has_commits`,
  `init`, `add_all`, `commit`, `has_changes`, `current_branch`,
  `branch_exists`, `create_branch`, `checkout`, `merge` (merges into whatever's
  currently checked out), `merged_branches`, `delete_branch`,
  `merged_remote_branches`, `delete_remote_branch`, `push`, `get_remote`/
  `set_remote`, `reachable_tags(ref)`, `unreleased_messages` (commits no tag
  contains yet), `commits_since`, `commits_between`, `create_tag`, `push_tag`.
  `push`/`push_tag` are best-effort: if no remote is configured yet (e.g.
  right after `git init`, before a repository exists on any platform), they
  silently no-op instead of raising — merging/releasing locally is still
  useful on its own.
- `infrastructure/git/adapter.py` — `GitAdapter(GitPort)`, subprocess-based.
  One concrete adapter, no sibling engines needed for local git itself.
- `domain/git/branching.py` — `BranchingConfig` + `branch_name()`/
  `initial_branches()`/`base_branch_name()`, read from `config/git.toml` via
  `infrastructure/git/config.py`'s `get_branching_config()`.
- `domain/git/commit.py` / `domain/git/version.py` — `ConventionalCommit`
  parsing (type, scope, breaking-change detection via `!` or a
  `BREAKING CHANGE:` footer) and `SemVer`/`VersionBump`/
  `detect_version_bump()` (breaking → major, any `feat` → minor, any
  `fix`/`perf` → patch, else none). The rules that turn a bump into a
  version live in `DetectNextVersionUseCase`, see below.
- `application/use_cases/git/` — `InitRepositoryUseCase`,
  `CreateFeatureBranchUseCase`, `MergeBranchUseCase`,
  `DetectNextVersionUseCase`, `CreateReleaseUseCase` (pure git: creates +
  pushes the `v{version}` tag), `CutMajorVersionUseCase` (creates the next
  major-version branch set from the current one's base branch — see
  "Breaking-change enforcement" below). The project's version lives only in
  `pyproject.toml` (`[project]` or `[tool.poetry]`, whichever is present) —
  `config/app.toml` no longer carries a `version`. Bumping it is **not** a
  `Port` method: `Config()` is read-only (no save path on
  `ConfigBase`/`TomlConfig`), so `infrastructure/git/version_file.py`
  writes it directly via `toml.load`/`toml.dump`, the same precedent
  `appcraft.utils.dependency_convert` uses for `pyproject.toml`.
  `infrastructure/git/config.py`'s `write_major_version()` does the same for
  `config/git.toml`'s `major_version` key.
- `runners/tools/git.py` — `init(use_major_version, major_version, stages,
  trunk_branch)` (what `GitTemplate.post_install` already invokes via
  `python tools git init`. Asks the setup questions in a terminal while
  `configured = false`, or takes the arguments, which skip the questions and
  are refused once configured; creates only the missing branches; also
  installs the `commit-msg` hook, see below), `start(kind, name)` (any Conventional Commits type),
  `merge(source, target)` (auto-redirects to the next major-version branch
  when `source` carries a breaking change, see below; creates a missing stage
  branch from the stage before it), `new_major()` (explicit major cut, same
  step as the automatic redirect), `changelog(output=None)` (Markdown of the
  unreleased commits, the ones the next release would contain, optionally
  prepended to a file),
  `cleanup()` (deletes merged work branches of the base, locally and on `origin`; asks unless `interactive=false`), and a major cut is always made above the highest existing major, and only when that major has a stable release (`new_major()` is refused before that; a breaking merge into the highest major is redirected to the next one only then, otherwise it merges normally, and a breaking merge into a lower major is refused with an alert when a higher one exists), `detect_version()`
  (read-only; shows what the current branch would release), `release()`
  (detects the next version for the current branch's stage, confirms,
  bumps `pyproject.toml`, commits, tags, and — only if `remote_repository`
  is installed *and* a remote is configured — creates a platform release
  too, marked pre-release when the version is one; a platform-release
  failure only warns, since the tag/commit already succeeded),
  `set_remote(url)`.

### Branching strategy (`config/git.toml`)

```toml
use_major_version = false   # branch names get a "v{N}-" prefix when true
major_version = 0           # current major line; only read when use_major_version = true
stages = ["alpha", "beta", "main"]   # ordered, least- to most-stable; empty = no stage concept
trunk_branch = "main"       # only used when stages = [] (single-branch case)
```

`use_major_version` and `stages` are independent booleans, so there are
exactly 4 supported combinations:

| case | config | example branch names |
|---|---|---|
| major + stage | `use_major_version=true`, `stages=[...]` | `v0-alpha`, `v0-beta`, `v0-main` |
| major only | `use_major_version=true`, `stages=[]` | `v0` |
| stage only | `use_major_version=false`, `stages=[...]` | `alpha`, `beta`, `main` |
| neither | `use_major_version=false`, `stages=[]` | `main` (from `trunk_branch`) |

The most-stable entry (`stages[-1]`, or `trunk_branch`/`v{N}` when there's no
stage list) is the **base branch** — `start(kind, name)` always creates
`{kind}/{name}` off of it, regardless of which stage it's merged into first.
This is a convention for *generated projects*, not for `appcraft` itself.

**Promotion workflow**: a feature/fix branch is merged into each stage
independently — e.g. `merge feat/x beta` to test, then later the *same*
branch `merge feat/x main` once validated — never a direct `beta → main`
merge. `MergeBranchUseCase` is generic (just `source`/`target`), so this
works for any number of configured stages, including zero.

### Breaking-change enforcement

When `use_major_version = true`, a branch like `v0-main` is a promise: no
breaking changes land there directly — they always go into a branch one
major version up. This is enforced at two layers:

1. **`merge(source, target)` auto-redirects.** Before merging, it checks
   `source`'s incoming commits (`GitPort.commits_between(target, source)`)
   for a breaking one. If found: `CutMajorVersionUseCase` creates
   **only** the next major line's entry (least-stable) branch — e.g.
   `v1-alpha` — from the *current* major's base (most-stable) branch, a
   no-op if it already exists. `v1-beta`/`v1-main` are deliberately not
   created yet: the new major line is unproven and has to earn promotion
   through the same stages as everything else, not start with a "stable"
   branch already in place. `config/git.toml`'s `major_version` is bumped
   **on the new branch only** (via `write_major_version()`, committed there
   — `v{N}-*`'s own `config/git.toml` is untouched, so it keeps resolving
   its own branch names correctly), and the merge is redirected there —
   **always to the entry branch**, regardless of which stage was originally
   targeted (merging a breaking change into `v0-beta` or `v0-main` both
   redirect to `v1-alpha`, never straight to `v1-beta`/`v1-main`).
   `v{N}-*` is never touched. This only triggers when `use_major_version`
   is enabled — with it off, breaking changes merge normally, there's no
   "branch above" to redirect to. `GitAdapter.merge()` passes `--no-verify`
   since the check below would otherwise block this *already-validated*
   merge too.
2. **The `commit-msg` git hook blocks everything else.** Most real commits
   never go through the runner — someone just runs `git commit`/`git merge`
   directly. `infrastructure/git/hooks/commit_msg.py` (installed as
   `.git/hooks/commit-msg` by `init()`, via `install_commit_msg_hook()`) is
   deliberately dependency-free (no `toml` import, no project imports — a
   hook must never break because some venv isn't active) and blocks *any*
   breaking commit, or merge bringing one in (checked via `.git/MERGE_HEAD`
   against the commits it would bring in), whenever the current branch
   matches the configured major-version naming pattern (`^v\d+(-.*)?$`) —
   full stop, regardless of which major number, with a message pointing at
   `python tools git merge`. It never tries to redirect anything
   itself — only the runner's own controlled flow above does that, since a
   hook silently moving a raw `git commit` to a different branch mid-command
   would be surprising and unsafe. A no-op when `use_major_version = false`.

### Conventional Commits + version detection

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `build:`,
`ci:`, `chore:`, `revert:`, with `!` or a `BREAKING CHANGE:` footer for
breaking changes). Release detection reads the **unreleased** commits: those
reachable from HEAD that no tag contains yet (`unreleased_messages()`), so a
promotion of commits that were already released on another stage adds nothing.
Each is parsed with `ConventionalCommit.parse()` and reduced to a bump with
`detect_version_bump()`.

### Stage-based releases (PEP 440)

The stage of the branch you run `release()` from picks the label: `alpha` →
`a`, `beta` → `b`, base → stable. Only the stage branches of the current major
line are valid (`initial_branches()`); anything else, e.g. a `feat/` branch, is
refused.

The **base** is the highest release of the line across every stage, so a
release from `main` sees releases cut on `alpha` and `beta`. The rules:

- **Major line without stages** (`stages = []`): the major branch is the only branch of the line, and every release is stable. Its first release is `M.0.0`, then the usual SemVer bumps.
- **Major line with stages and no release yet** (`use_major_version = true`): the first
  release is always `M.0.0<label>1`, where the label is the least stable stage's (`a` for alpha, `b` for beta), and it must come from that stage: the first entry of `stages`. A config with only `beta` and `main` starts a major as `M.0.0b1`. Minor and
  patch bumps only start after it.
- **Base is a pre-release `X`:** a `fix:` stays in the same version (`0.6.0a1`
  → `0.6.0a2`). A `feat:` or breaking change opens the next one (`0.6.0a2` →
  `0.7.0a1`). Promoting the same commits to a later stage keeps the version
  (`0.8.0a1` → `0.8.0b1` → `0.8.0`). No new commits on the same stage: nothing
  to release.
- **Base is stable `S`:** plain SemVer from `S` (`0.8.0` → `0.8.1a1` for a
  fix, `0.9.0a1` for a feature, `1.0.0a1` for a breaking change).
- **Breaking change before any stable release** is a minor bump, whatever
  pre-releases exist (`0.1.0a1` → `0.2.0a1`). A breaking change is a major bump
  only after a stable release exists.
- **Labels count on their own:** the counter is per label and per target
  version, so the second alpha of `0.6.0` is `0.6.0a2`.
- A version can stop at any stage: `0.6.0a1` with no beta and no stable is
  valid.

The version written to `pyproject.toml` and the tag (`v0.7.0a1`) use the same
PEP 440 string, so pip and poetry resolve pre-releases as usual (`pip install`
skips them unless `--pre`).

## `remote_repository` (active, `standalone = False`, `dependencies = ["git"]`)

The shared foundation for hosting-platform support — install `github`
(depends on this one) instead; `remote_repository` itself is rejected if
requested directly (`TemplateNotStandaloneError`), since alone it has no
platform adapter to talk to anything.

- `application/ports/remote_repository.py` — `RemoteRepositoryPort`:
  `is_available` (CLI installed + authenticated), `create_repository`,
  `get_repository`, `delete_repository`, `create_release`. Platform-agnostic
  — shared by every concrete adapter, never GitHub-specific.
- `domain/remote_repository/repo.py` — `RemoteRepo` (plain frozen
  dataclass: `name`, `url`, `description`, `is_private`), named to avoid
  colliding with the architecture's `Repository`-suffix convention (an
  `application/`-layer concept) — this is a plain external-resource value
  object, same spirit as `domain/web_scraping/session.py`.
- `infrastructure/remote_repository/provider.py` —
  `get_default_remote_repository_adapter()`, mirroring
  `infrastructure/database/provider.py`'s `_ADAPTER_BACKENDS` /
  `infrastructure/web_scraping/provider.py`'s `_INTERACTIVE_BACKENDS`:
  `_PLATFORM_BACKENDS` maps `"github"` (and, later, `"gitlab"`/
  `"bitbucket"`) to `(template_module, template_class, adapter_module,
  adapter_getter_name)`, resolved via each candidate's own `is_installed()`.
  `config/remote_repository.toml`'s `default_platform` breaks the tie when
  more than one platform is installed; returns `None` if none are.
- `presentation/cli/remote_repository.py` /
  `runners/tools/remote_repository.py` — **the one generic runner**:
  `create_repo(...)` (creates on whichever platform is installed, then
  wires the local `origin` remote via `GitPort.set_remote()`),
  `delete_repo(...)`. Platform-specific templates (`github`, future
  `gitlab`/`bitbucket`) contribute **no runner of their own** — this is the
  only one, for every platform.

### `config/remote_repository.toml`

```toml
default_platform = "github"   # github, gitlab or bitbucket — picks which installed adapter the generic runner/provider use by default
```

Same shape/role as `config/web_scraping.toml`'s `default_interactive_adapter`.

## `github` (active, `dependencies = ["remote_repository"]`)

Contributes only `infrastructure/remote_repository/github/adapter.py` —
`GitHubAdapter(RemoteRepositoryPort)`, wrapping the `gh` CLI
(`infrastructure/<concept>/<engine>/adapter.py`, exactly like
`infrastructure/web_scraping/selenium/adapter.py`), plus
`get_github_adapter()` (shared-singleton getter, same shape as
`get_sqlalchemy_adapter()`). No domain/application/presentation/runner
files of its own — everything else lives in `remote_repository`.
