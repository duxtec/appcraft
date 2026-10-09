from dataclasses import dataclass

from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.git.commit import ConventionalCommit
from domain.git.version import SemVer


@dataclass(frozen=True)
class UnreleasedCommits:
    latest: SemVer | None
    commits: list[ConventionalCommit]


class ListUnreleasedCommitsUseCase(UseCase[tuple[str, ...], UnreleasedCommits]):
    """The commits the next release would contain: those no tag contains yet.
    `latest` is the highest release reachable from the given stage branches,
    for context."""

    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: tuple[str, ...]) -> UnreleasedCommits:
        latest: SemVer | None = None
        for ref in input_data:
            for tag in self.git.reachable_tags(ref):
                try:
                    version = SemVer.parse(tag)
                except ValueError:
                    continue
                if latest is None or version.sort_key > latest.sort_key:
                    latest = version

        return UnreleasedCommits(
            latest=latest,
            commits=[
                ConventionalCommit.parse(message)
                for message in self.git.unreleased_messages()
            ],
        )
