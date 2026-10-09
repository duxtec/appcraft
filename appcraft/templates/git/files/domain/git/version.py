import re
from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from domain.git.commit import ConventionalCommit, ConventionalCommitType

_VERSION_PATTERN = re.compile(
    r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:(?P<label>a|b|rc)(?P<number>\d+))?$"
)

# Stage branch name -> PEP 440 pre-release label. `stable` (the base stage)
# has no label and produces a plain release.
PRERELEASE_LABELS = {"alpha": "a", "beta": "b", "rc": "rc"}

_PATCH_TYPES = (ConventionalCommitType.FIX, ConventionalCommitType.PERF)


class VersionBump(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    NONE = "none"


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int
    label: str | None = None
    number: int = 0

    @classmethod
    def parse(cls, text: str) -> "SemVer":
        match = _VERSION_PATTERN.match(text.strip())
        if match is None:
            raise ValueError(f"'{text}' is not a valid version")

        return cls(
            major=int(match.group("major")),
            minor=int(match.group("minor")),
            patch=int(match.group("patch")),
            label=match.group("label"),
            number=int(match.group("number") or 0),
        )

    @property
    def is_prerelease(self) -> bool:
        return self.label is not None

    @property
    def stable(self) -> "SemVer":
        return SemVer(self.major, self.minor, self.patch)

    @property
    def sort_key(self) -> tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def bump(self, bump: VersionBump) -> "SemVer":
        if bump is VersionBump.MAJOR:
            return SemVer(self.major + 1, 0, 0)
        if bump is VersionBump.MINOR:
            return SemVer(self.major, self.minor + 1, 0)
        if bump is VersionBump.PATCH:
            return SemVer(self.major, self.minor, self.patch + 1)
        return self

    def with_prerelease(self, label: str, number: int) -> "SemVer":
        return SemVer(self.major, self.minor, self.patch, label, number)

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.label is not None:
            version += f"{self.label}{self.number}"
        return version


def detect_version_bump(commits: Sequence[ConventionalCommit]) -> VersionBump:
    if any(commit.is_breaking for commit in commits):
        return VersionBump.MAJOR
    if any(commit.type is ConventionalCommitType.FEAT for commit in commits):
        return VersionBump.MINOR
    if any(commit.type in _PATCH_TYPES for commit in commits):
        return VersionBump.PATCH
    return VersionBump.NONE
