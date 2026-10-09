from typing import Sequence

from domain.git.commit import ConventionalCommit, ConventionalCommitType


def render_changelog(commits: Sequence[ConventionalCommit], title: str) -> str:
    breaking = [c for c in commits if c.is_breaking]
    features = _of_type(commits, ConventionalCommitType.FEAT, breaking)
    fixes = _of_type(commits, ConventionalCommitType.FIX, breaking)
    performance = _of_type(commits, ConventionalCommitType.PERF, breaking)
    others = [
        c
        for c in commits
        if not c.is_breaking
        and c.type is not None
        and c.type not in (ConventionalCommitType.FEAT, ConventionalCommitType.FIX, ConventionalCommitType.PERF)
        and not (c.type is ConventionalCommitType.CHORE and c.scope == "release")
    ]

    sections = [
        ("Breaking changes", breaking),
        ("Features", features),
        ("Fixes", fixes),
        ("Performance", performance),
        ("Other changes", others),
    ]

    lines = [f"## {title}", ""]
    if not any(items for _, items in sections):
        lines += ["No changes.", ""]
    for heading, items in sections:
        if not items:
            continue
        lines += [f"### {heading}", ""]
        lines += [f"- {_describe(c)}" for c in items]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _of_type(
    commits: Sequence[ConventionalCommit],
    commit_type: ConventionalCommitType,
    breaking: Sequence[ConventionalCommit],
) -> list[ConventionalCommit]:
    return [c for c in commits if c.type is commit_type and c not in breaking]


def _describe(commit: ConventionalCommit) -> str:
    if commit.scope:
        return f"**{commit.scope}:** {commit.description}"
    return commit.description
