#!/usr/bin/env python3
"""Blocks a breaking-change commit (or merge bringing one in) directly on
a major-version branch (e.g. 'v0-main').

Installed as .git/hooks/commit-msg by the `git init` runner command
(infrastructure.git.hooks.install_commit_msg_hook). Deliberately
dependency-free — no toml library, no project imports — so it keeps
working regardless of which Python/venv happens to invoke a raw `git
commit`/`git merge`. A breaking change should instead be made on a
feat/fix branch and merged in via `python tools git merge`, which
automatically cuts the next major-version branch line for it instead of
landing the breaking commit here.
"""
import os
import re
import subprocess
import sys

_BREAKING_HEADER = re.compile(r"^\w+(\([^)]+\))?!:")
_BREAKING_FOOTER = re.compile(r"^BREAKING[ -]CHANGE:", re.MULTILINE)
_MAJOR_BRANCH = re.compile(r"^v(\d+)(-.*)?$")
_STABLE_TAG = r"v{major}\.\d+\.\d+"


def _config() -> str:
    try:
        with open("config/git.toml", "r") as f:
            return f.read()
    except OSError:
        return ""


def _uses_major_version_branches(content: str) -> bool:
    match = re.search(
        r"^\s*use_major_version\s*=\s*(true|false)\b",
        content,
        re.MULTILINE,
    )
    return bool(match and match.group(1) == "true")


def _line_has_stable_release(major: int, content: str) -> bool:
    """A breaking change is only refused once the line has shipped a stable
    release: the stable tag must be reachable from the line's base branch."""
    stages = re.search(r"^\s*stages\s*=\s*\[([^\]]*)\]", content, re.MULTILINE)
    names = re.findall(r'"([^"]+)"', stages.group(1)) if stages else []
    base = f"v{major}-{names[-1]}" if names else f"v{major}"

    result = subprocess.run(
        ["git", "tag", "--merged", base],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return False

    stable = re.compile(_STABLE_TAG.format(major=major))
    return any(stable.fullmatch(tag.strip()) for tag in result.stdout.splitlines())


def _current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def _merge_head() -> str | None:
    try:
        with open(os.path.join(".git", "MERGE_HEAD"), "r") as f:
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
    return [m.strip() for m in result.stdout.split("\x1e") if m.strip()]


def _is_breaking(message: str) -> bool:
    header, _, body = message.partition("\n")
    return bool(
        _BREAKING_HEADER.match(header.strip())
        or _BREAKING_FOOTER.search(body)
    )


def main() -> int:
    content = _config()
    if not _uses_major_version_branches(content):
        return 0

    branch = _current_branch()
    match = _MAJOR_BRANCH.match(branch)
    if not match:
        return 0

    messages = _incoming_messages(_merge_head(), sys.argv[1])
    if not any(_is_breaking(message) for message in messages):
        return 0

    if not _line_has_stable_release(int(match.group(1)), content):
        return 0

    sys.stderr.write(
        f"\nBreaking changes are not allowed directly on '{branch}' "
        "(a major-version branch).\n"
        "Make the change on a feat/fix branch and merge it in via "
        f"`python tools git merge <branch> {branch}` instead — that "
        "automatically cuts the next major-version branch line for "
        "it.\n\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
