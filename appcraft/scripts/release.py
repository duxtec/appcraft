"""Dev-only release tooling for the appcraft repo itself.

appcraft's own repo isn't a generated Clean Architecture project, so it
can't `appcraft init`/`add_template` the `git`/`remote_repository`/`github`
templates onto itself the normal way: their `runners/tools/git.py` depends
on the generated project's own runner/config system
(`infrastructure/core/runner`, `Config()`), which doesn't exist here.

Their actual business logic — branching rules, Conventional Commits
parsing, PEP 440 version detection, the `git`/`gh` subprocess adapters —
has no such dependency (confirmed empirically: the only third-party import
anywhere in that chain is `pydantic`, transitively via
`application.use_cases.UseCase`'s sibling `ReadUseCase` needing
`domain.filters.interface.Filter`, hence the `dev` dependency added
alongside this script). So this script reuses that logic directly instead
of duplicating it: it merges the four templates' `files/` trees into a
throwaway scratch directory via `TemplateAdder` — the same mechanism
`add_template` itself uses — adds that directory to `sys.path`, and runs
against the real appcraft repo as the target.

Configured for appcraft's own branching: major-version branches
(`v{N}-{stage}`), stages = (beta, main) — no alpha for now. major_version
is never persisted: it's read off the current branch name (for
detect-version/release) or off the highest `v{N}-*` branch that exists
(for start/merge/new-major), so there's no config file to keep in sync.

Usage: python appcraft/scripts/release.py <command> [options]
"""

import argparse
import importlib
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGES = ("beta", "main")

os.chdir(REPO_ROOT)  # write_pyproject_version/the commit-msg hook/`gh`
# all resolve paths relative to the process cwd, not to repo_path below.
sys.path.insert(0, str(REPO_ROOT))
from appcraft.utils.template.adder import (  # noqa: E402
    TemplateAdder,  # pyright: ignore[reportMissingTypeStubs]
)

_scratch = Path(tempfile.mkdtemp(prefix="appcraft-release-"))
_adder = TemplateAdder(target_dir=_scratch)
for _name in ("base", "git", "remote_repository", "github"):
    _adder.add_template(_name)
sys.path.insert(0, str(_scratch))


def _dynamic(module_path: str, *names: str) -> Any:
    """Imports a name from one of the templates merged into `_scratch`
    above. Plain `from X import Y` can't be used for these: pyright (like
    CPython at runtime) resolves `application.use_cases`/`application.ports`
    as regular packages rooted in `base`'s own directory alone, so a
    submodule that physically lives under `git`'s/`github`'s/
    `remote_repository`'s directory (e.g. `application.use_cases.git.*`)
    is only resolvable once all four are copied into one real directory,
    which only exists at runtime. `importlib` sidesteps static resolution
    entirely instead of producing an unresolved-import error that strict
    mode would then cascade into dozens of "Unknown type" errors at every
    call site."""
    module = importlib.import_module(module_path)
    values = [getattr(module, name) for name in names]
    return values[0] if len(values) == 1 else tuple(values)


CreateFeatureBranchInput, CreateFeatureBranchUseCase = _dynamic(
    "application.use_cases.git.create_feature_branch",
    "CreateFeatureBranchInput",
    "CreateFeatureBranchUseCase",
)
CreateReleaseUseCase = _dynamic(
    "application.use_cases.git.create_release", "CreateReleaseUseCase"
)
CutMajorVersionUseCase = _dynamic(
    "application.use_cases.git.cut_major_version", "CutMajorVersionUseCase"
)
DeleteBranchesUseCase = _dynamic(
    "application.use_cases.git.delete_branches", "DeleteBranchesUseCase"
)
DetectNextInput, DetectNextVersionUseCase = _dynamic(
    "application.use_cases.git.detect_next_version",
    "DetectNextInput",
    "DetectNextVersionUseCase",
)
ListCleanupBranchesUseCase = _dynamic(
    "application.use_cases.git.list_cleanup_branches",
    "ListCleanupBranchesUseCase",
)
ListUnreleasedCommitsUseCase = _dynamic(
    "application.use_cases.git.list_unreleased_commits",
    "ListUnreleasedCommitsUseCase",
)
MergeBranchInput, MergeBranchUseCase = _dynamic(
    "application.use_cases.git.merge_branch",
    "MergeBranchInput",
    "MergeBranchUseCase",
)
FirstReleaseNotEntryError, NotAReleaseBranchError = _dynamic(
    "domain.exceptions.git",
    "FirstReleaseNotEntryError",
    "NotAReleaseBranchError",
)
(
    BranchingConfig,
    base_branch_name,
    entry_branch_name,
    initial_branches,
    previous_stage_branch,
    stage_of_branch,
) = _dynamic(
    "domain.git.branching",
    "BranchingConfig",
    "base_branch_name",
    "entry_branch_name",
    "initial_branches",
    "previous_stage_branch",
    "stage_of_branch",
)
render_changelog = _dynamic("domain.git.changelog", "render_changelog")
ConventionalCommit, ConventionalCommitType = _dynamic(
    "domain.git.commit", "ConventionalCommit", "ConventionalCommitType"
)
PRERELEASE_LABELS, SemVer = _dynamic(
    "domain.git.version", "PRERELEASE_LABELS", "SemVer"
)
GitAdapter = _dynamic("infrastructure.git.adapter", "GitAdapter")
write_pyproject_version = _dynamic(
    "infrastructure.git.version_file", "write_pyproject_version"
)
GitHubAdapter = _dynamic(
    "infrastructure.remote_repository.github.adapter", "GitHubAdapter"
)

_COMMIT_MSG_HOOK = '''#!/usr/bin/env python3
"""Blocks a breaking-change commit (or merge bringing one in) directly on
a major-version branch (e.g. 'v1-main').

Installed as .git/hooks/commit-msg by
`python appcraft/scripts/release.py install-hook`. Deliberately
dependency-free — no project imports — so it keeps working regardless of
which Python/venv happens to invoke a raw `git commit`/`git merge`. A
breaking change should instead be made on a feat/fix branch and merged in
via `python appcraft/scripts/release.py merge <branch> <target>`, which
automatically cuts the next major-version branch line for it instead of
landing the breaking commit here.

Hardcoded for appcraft's own branching (stages = beta, main — no alpha),
unlike the generated-project version of this hook, which reads
config/git.toml: appcraft's own repo has no such file.
"""
import re
import subprocess
import sys

_BREAKING_HEADER = re.compile(r"^\\w+(\\([^)]+\\))?!:")
_BREAKING_FOOTER = re.compile(r"^BREAKING[ -]CHANGE:", re.MULTILINE)
_MAJOR_BRANCH = re.compile(r"^v(\\d+)(-.*)?$")
_STABLE_TAG = r"v{major}\\.\\d+\\.\\d+"
_BASE_STAGE = "main"


def _line_has_stable_release(major: int) -> bool:
    base = f"v{major}-{_BASE_STAGE}"
    result = subprocess.run(
        ["git", "tag", "--merged", base], text=True, capture_output=True
    )
    if result.returncode != 0:
        return False
    stable = re.compile(_STABLE_TAG.format(major=major))
    return any(
        stable.fullmatch(tag.strip()) for tag in result.stdout.splitlines()
    )


def _current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"], text=True, capture_output=True
    )
    return result.stdout.strip()


def _merge_head() -> str | None:
    try:
        with open(".git/MERGE_HEAD", "r") as f:
            return f.read().strip()
    except OSError:
        return None


def _incoming_messages(merge_head: str | None, message_file: str) -> list[str]:
    if merge_head is None:
        with open(message_file, "r") as f:
            return [f.read()]
    result = subprocess.run(
        ["git", "log", f"HEAD..{merge_head}", "--pretty=format:%B%x1e"],
        text=True,
        capture_output=True,
    )
    return [m.strip() for m in result.stdout.split("\\x1e") if m.strip()]


def _is_breaking(message: str) -> bool:
    header, _, body = message.partition("\\n")
    return bool(
        _BREAKING_HEADER.match(header.strip()) or _BREAKING_FOOTER.search(body)
    )


def main() -> int:
    branch = _current_branch()
    match = _MAJOR_BRANCH.match(branch)
    if not match:
        return 0

    messages = _incoming_messages(_merge_head(), sys.argv[1])
    if not any(_is_breaking(message) for message in messages):
        return 0

    if not _line_has_stable_release(int(match.group(1))):
        return 0

    sys.stderr.write(
        f"\\nBreaking changes are not allowed directly on '{branch}' "
        "(a major-version branch).\\n"
        "Make the change on a feat/fix branch and merge it in via "
        f"`python appcraft/scripts/release.py merge <branch> {branch}` "
        "instead — that automatically cuts the next major-version branch "
        "line for it.\\n\\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
'''


def _config(major_version: int) -> Any:
    return BranchingConfig(
        use_major_version=True, major_version=major_version, stages=STAGES
    )


def _major_of_branch(branch: str | None) -> int:
    match = re.match(r"^v(\d+)", branch or "")
    return int(match.group(1)) if match else 0


def _top_major(git: Any) -> int:
    majors = [
        int(match.group(1))
        for branch in git.list_branches()
        if (match := re.match(r"^v(\d+)", branch))
    ]
    return max(majors, default=0)


def _has_stable_release(git: Any, config: Any) -> bool:
    base = base_branch_name(config)
    for tag in git.reachable_tags(base):
        try:
            version = SemVer.parse(tag)
        except ValueError:
            continue
        if not version.is_prerelease and version.major == config.major_version:
            return True
    return False


def _cut_next_major(git: Any, config: Any) -> Any:
    new_config = CutMajorVersionUseCase(git).execute(config)
    git.checkout(entry_branch_name(new_config))
    return new_config


def _release_label(git: Any, config: Any) -> str | None:
    branch = git.current_branch()
    if branch not in initial_branches(config):
        raise NotAReleaseBranchError(branch)
    stage = stage_of_branch(config, branch)
    if stage is None:
        return None
    if stage not in PRERELEASE_LABELS:
        raise NotAReleaseBranchError(branch)
    return PRERELEASE_LABELS[stage]


def _next_version(git: Any) -> Any:
    major = _major_of_branch(git.current_branch())
    config = _config(major)
    label = _release_label(git, config)
    refs = tuple(
        branch
        for branch in initial_branches(config)
        if git.branch_exists(branch)
    ) or ("HEAD",)
    return DetectNextVersionUseCase(git).execute(
        DetectNextInput(
            label=label,
            refs=refs,
            line_major=major,
            entry_stage=config.entry_stage,
            entry_label=PRERELEASE_LABELS.get(config.entry_stage or ""),
        )
    )


def _confirmed(question: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    return input(f"{question} (y/N): ").strip().lower() in ("y", "yes")


def cmd_install_hook(git: Any, args: argparse.Namespace) -> None:
    hooks_dir = REPO_ROOT / ".git" / "hooks"
    target = hooks_dir / "commit-msg"
    if target.exists() and not args.force:
        print(f"'{target}' already exists — pass --force to overwrite.")
        return
    target.write_text(_COMMIT_MSG_HOOK)
    target.chmod(target.stat().st_mode | 0o111)
    print(f"Installed commit-msg hook at '{target}'.")


def cmd_start(git: Any, args: argparse.Namespace) -> None:
    valid_kinds = [
        commit_type.value for commit_type in ConventionalCommitType
    ]
    if args.kind not in valid_kinds:
        print(
            f"'{args.kind}' is not a Conventional Commits type. Use one "
            "of: " + ", ".join(valid_kinds)
        )
        sys.exit(1)

    config = _config(_top_major(git))
    base_branch = base_branch_name(config)
    branch = CreateFeatureBranchUseCase(git).execute(
        CreateFeatureBranchInput(
            kind=args.kind, name=args.name, base_branch=base_branch
        )
    )
    print(f"Created '{branch}' from '{base_branch}'.")


def cmd_merge(git: Any, args: argparse.Namespace) -> None:
    source, target = args.source, args.target
    top_config = _config(_top_major(git))

    if not git.branch_exists(target):
        source_stage = previous_stage_branch(top_config, target)
        if source_stage is not None:
            git.create_branch(target, source=source_stage)
            print(f"Created stage branch '{target}' from '{source_stage}'.")

    incoming = git.commits_between(target, source)
    is_breaking = any(
        ConventionalCommit.parse(message).is_breaking for message in incoming
    )

    target_major = _major_of_branch(target)
    if is_breaking and target_major < top_config.major_version:
        print(
            f"'{target}' isn't the highest major line — a higher one "
            f"({base_branch_name(top_config)}) already exists. Merge the "
            "breaking change there instead."
        )
        return
    if is_breaking and _has_stable_release(git, top_config):
        new_config = _cut_next_major(git, top_config)
        new_target = entry_branch_name(new_config)
        print(
            f"Breaking change: redirecting merge from '{target}' to "
            f"'{new_target}'."
        )
        target = new_target

    MergeBranchUseCase(git).execute(
        MergeBranchInput(source=source, target=target)
    )
    print(f"Merged '{source}' into '{target}'.")


def cmd_detect_version(git: Any, args: argparse.Namespace) -> None:
    try:
        version = _next_version(git)
    except (NotAReleaseBranchError, FirstReleaseNotEntryError) as e:
        print(str(e))
        return
    if version is None:
        print("No releasable changes since the last tag.")
        return
    print(f"Next version: v{version}")


def _release_notes(git: Any, version: Any) -> str:
    config = _config(_major_of_branch(git.current_branch()))
    refs = tuple(
        branch
        for branch in initial_branches(config)
        if git.branch_exists(branch)
    ) or ("HEAD",)
    unreleased = ListUnreleasedCommitsUseCase(git).execute(refs)
    notes = render_changelog(unreleased.commits, f"v{version}")
    changelog_url = (
        f"https://duxtec.github.io/appcraft/{version}/changelog.html"
    )
    return f"{notes}\nFull changelog: {changelog_url}\n"


def cmd_release(git: Any, args: argparse.Namespace) -> None:
    try:
        version = _next_version(git)
    except (NotAReleaseBranchError, FirstReleaseNotEntryError) as e:
        print(str(e))
        return
    if version is None:
        print("No releasable changes since the last tag.")
        return

    print(f"Next version: v{version}")
    if not _confirmed(f"Release v{version}?", args.yes):
        return

    # Computed before tagging: ListUnreleasedCommitsUseCase means "no tag
    # contains it yet", so calling this after CreateReleaseUseCase creates
    # the tag below would see nothing — the exact commits this release
    # notes block needs to describe.
    notes = _release_notes(git, version)

    write_pyproject_version(str(version))
    git.add_all()
    if git.has_changes():
        git.commit(f"chore(release): v{version}")
        git.push(git.current_branch())

    tag = CreateReleaseUseCase(git).execute(version)
    print(f"Tagged and pushed {tag}.")

    github = GitHubAdapter()
    if git.get_remote() is not None:
        if not version.is_prerelease:
            _promote_default_branch(git, github, version)
        try:
            url = github.create_release(
                tag=tag,
                title=tag,
                notes=notes,
                prerelease=version.is_prerelease,
            )
            print(f"GitHub release: {url}")
        except Exception as e:
            print(f"Tag/commit succeeded, but the GitHub release failed: {e}")


def _promote_default_branch(git: Any, github: Any, version: Any) -> None:
    branch = git.current_branch()
    try:
        current_default = github.get_default_branch()
    except Exception as e:
        print(f"Could not read the current default branch: {e}")
        return
    if current_default == branch or (
        version.major <= _major_of_branch(current_default)
    ):
        return
    try:
        git.push(branch)
        github.set_default_branch(branch)
    except Exception as e:
        print(f"Could not promote the default branch: {e}")
        return
    print(f"Default branch promoted: '{current_default}' -> '{branch}'.")


def cmd_new_major(git: Any, args: argparse.Namespace) -> None:
    top_config = _config(_top_major(git))
    if not _has_stable_release(git, top_config):
        print(
            f"Major {top_config.major_version} has no stable release yet — "
            "can't cut a new major line above it."
        )
        return
    new_config = _cut_next_major(git, top_config)
    print(
        f"Cut '{entry_branch_name(new_config)}' "
        f"(major {new_config.major_version})."
    )


def cmd_changelog(git: Any, args: argparse.Namespace) -> None:
    config = _config(_top_major(git))
    refs = tuple(
        branch
        for branch in initial_branches(config)
        if git.branch_exists(branch)
    ) or ("HEAD",)
    unreleased = ListUnreleasedCommitsUseCase(git).execute(refs)
    title = (
        f"Unreleased changes since {unreleased.latest}"
        if unreleased.latest
        else "Unreleased changes"
    )
    text = render_changelog(unreleased.commits, title)
    print(text)
    if args.output:
        try:
            existing = Path(args.output).read_text()
        except FileNotFoundError:
            existing = ""
        Path(args.output).write_text(text + "\n" + existing)
        print(f"Prepended to '{args.output}'.")


def cmd_cleanup(git: Any, args: argparse.Namespace) -> None:
    config = _config(_top_major(git))
    stable = base_branch_name(config)
    if not git.branch_exists(stable):
        print("Nothing to clean up.")
        return

    candidates = ListCleanupBranchesUseCase(git).execute(stable)
    if not candidates.local and not candidates.remote:
        print("Nothing to clean up.")
        return

    if candidates.local:
        print(f"Local branches merged into '{stable}':")
        for branch in candidates.local:
            print(f"  - {branch}")
    if candidates.remote:
        print(f"Remote branches on origin merged into '{stable}':")
        for branch in candidates.remote:
            print(f"  - origin/{branch}")
    if not _confirmed("Delete them?", args.yes):
        return

    DeleteBranchesUseCase(git).execute(candidates)
    deleted = len(candidates.local) + len(candidates.remote)
    print(f"Deleted {deleted} branch(es).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Assume yes on every confirmation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_hook_parser = subparsers.add_parser(
        "install-hook", help="Install the commit-msg hook."
    )
    install_hook_parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing hook."
    )

    start_parser = subparsers.add_parser(
        "start",
        help="Create a feat/fix/... branch off the current major's base.",
    )
    start_parser.add_argument("kind")
    start_parser.add_argument("name")

    merge_parser = subparsers.add_parser(
        "merge", help="Merge a branch into a stage, with major redirect."
    )
    merge_parser.add_argument("source")
    merge_parser.add_argument("target")

    subparsers.add_parser(
        "detect-version", help="Show the next version without releasing."
    )
    subparsers.add_parser(
        "release", help="Detect, tag, push and create a GitHub release."
    )
    subparsers.add_parser(
        "new-major", help="Cut the next major line's entry branch."
    )

    changelog_parser = subparsers.add_parser(
        "changelog", help="Render unreleased changes."
    )
    changelog_parser.add_argument("output", nargs="?", default=None)

    subparsers.add_parser(
        "cleanup", help="Delete merged work branches, local and remote."
    )

    args = parser.parse_args()

    git = GitAdapter(repo_path=str(REPO_ROOT))
    commands: dict[str, Callable[[Any, argparse.Namespace], None]] = {
        "install-hook": cmd_install_hook,
        "start": cmd_start,
        "merge": cmd_merge,
        "detect-version": cmd_detect_version,
        "release": cmd_release,
        "new-major": cmd_new_major,
        "changelog": cmd_changelog,
        "cleanup": cmd_cleanup,
    }
    try:
        commands[args.command](git, args)
    finally:
        shutil.rmtree(_scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
