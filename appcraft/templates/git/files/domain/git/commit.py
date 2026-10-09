import re
from dataclasses import dataclass
from enum import Enum


class ConventionalCommitType(str, Enum):
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    REVERT = "revert"


_HEADER_PATTERN = re.compile(
    r"^(?P<type>\w+)(\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<description>.+)$"  # noqa: E501
)
_BREAKING_FOOTER_PATTERN = re.compile(r"^BREAKING[ -]CHANGE:", re.MULTILINE)


@dataclass(frozen=True)
class ConventionalCommit:
    type: ConventionalCommitType | None
    scope: str | None
    description: str
    is_breaking: bool
    raw: str

    @classmethod
    def parse(cls, message: str) -> "ConventionalCommit":
        header, _, body = message.partition("\n")
        match = _HEADER_PATTERN.match(header.strip())

        if match is None:
            return cls(
                type=None,
                scope=None,
                description=header.strip(),
                is_breaking=bool(_BREAKING_FOOTER_PATTERN.search(body)),
                raw=message,
            )

        raw_type = match.group("type").lower()
        try:
            commit_type = ConventionalCommitType(raw_type)
        except ValueError:
            commit_type = None

        is_breaking = bool(
            match.group("breaking")
            or _BREAKING_FOOTER_PATTERN.search(body)
        )

        return cls(
            type=commit_type,
            scope=match.group("scope"),
            description=match.group("description").strip(),
            is_breaking=is_breaking,
            raw=message,
        )
