from dataclasses import dataclass

from application.ports.git import GitPort
from application.use_cases import UseCase
from domain.exceptions.git import FirstReleaseNotEntryError
from domain.git.commit import ConventionalCommit
from domain.git.version import SemVer, VersionBump, detect_version_bump

_STAGE_RANK = {"a": 0, "b": 1, "rc": 2}
_STABLE_RANK = 3


def _rank(version: SemVer) -> int:
    return _STABLE_RANK if version.label is None else _STAGE_RANK[version.label]


@dataclass(frozen=True)
class DetectNextInput:
    """`label` is None for a stable release, or a PEP 440 label ('a', 'b',
    'rc'). `refs` are the stage branches of the line; the releases of the
    line are the tags reachable from any of them. `line_major` is the major
    of the current line when major version branches are in use, and
    `entry_stage` is that line's least stable stage with its label, the only
    place its first release can come from."""

    label: str | None
    refs: tuple[str, ...] = ("HEAD",)
    line_major: int | None = None
    entry_stage: str | None = None
    entry_label: str | None = None


class DetectNextVersionUseCase(UseCase[DetectNextInput, SemVer | None]):
    """Next version to release.

    The base is the highest release across every stage of the line. After a
    pre-release `X`, fixes stay in the same version train, and features or
    breaking changes open the next one. After a stable release, the bump is
    plain SemVer. A breaking change only becomes a major once a stable
    release exists; before that it bumps the minor.
    """

    def __init__(self, git: GitPort) -> None:
        self.git = git

    def execute(self, input_data: DetectNextInput) -> SemVer | None:
        releases = self._releases(input_data.refs, input_data.line_major)

        if input_data.line_major is not None and not releases:
            if input_data.entry_stage is None:
                return SemVer(input_data.line_major, 0, 0)
            if input_data.entry_label is None or input_data.label != input_data.entry_label:
                raise FirstReleaseNotEntryError(
                    input_data.line_major, input_data.entry_stage, input_data.entry_label
                )
            return SemVer(input_data.line_major, 0, 0, input_data.entry_label, 1)

        bump = detect_version_bump(self._unreleased())
        has_stable = any(not version.is_prerelease for version in releases)
        bump = self._before_first_stable(bump, has_stable)

        if not releases:
            if bump is VersionBump.NONE:
                return None
            return self._labelled(SemVer(0, 0, 0).bump(bump), input_data.label, releases)

        highest = max(releases, key=lambda version: (version.sort_key, _rank(version)))

        if highest.is_prerelease:
            if bump is VersionBump.NONE:
                promoting = input_data.label is None or _rank_label(input_data.label) > _rank(highest)
                if not promoting:
                    return None
                return self._labelled(highest.stable, input_data.label, releases)
            if bump is VersionBump.PATCH:
                return self._labelled(highest.stable, input_data.label, releases)
            return self._labelled(highest.stable.bump(bump), input_data.label, releases)

        if bump is VersionBump.NONE:
            return None
        return self._labelled(highest.bump(bump), input_data.label, releases)

    @staticmethod
    def _before_first_stable(bump: VersionBump, has_stable: bool) -> VersionBump:
        """Until the first stable release, the API isn't in production yet,
        so a breaking change only bumps the minor."""
        if bump is VersionBump.MAJOR and not has_stable:
            return VersionBump.MINOR
        return bump

    def _labelled(
        self, target: SemVer, label: str | None, releases: list[SemVer]
    ) -> SemVer:
        if label is None:
            return target
        existing = [
            version.number
            for version in releases
            if version.label == label and version.stable == target.stable
        ]
        return target.with_prerelease(label, max(existing, default=0) + 1)

    def _unreleased(self) -> list[ConventionalCommit]:
        return [ConventionalCommit.parse(message) for message in self.git.unreleased_messages()]

    def _releases(self, refs: tuple[str, ...], line_major: int | None) -> list[SemVer]:
        seen: set[str] = set()
        releases: list[SemVer] = []
        for ref in refs:
            for tag in self.git.reachable_tags(ref):
                if tag in seen:
                    continue
                seen.add(tag)
                try:
                    version = SemVer.parse(tag)
                except ValueError:
                    continue
                if line_major is None or version.major == line_major:
                    releases.append(version)
        return releases


def _rank_label(label: str) -> int:
    return _STAGE_RANK[label]
