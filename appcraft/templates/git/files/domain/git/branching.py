import re
from dataclasses import dataclass


@dataclass(frozen=True)
class BranchingConfig:
    use_major_version: bool = False
    major_version: int = 0
    stages: tuple[str, ...] = ()
    trunk_branch: str = "main"

    @property
    def base_stage(self) -> str | None:
        """The most-stable configured stage (feat/fix branches are always
        created from the branch this resolves to via `branch_name()`)."""
        return self.stages[-1] if self.stages else None

    @property
    def entry_stage(self) -> str | None:
        """The least-stable configured stage — where a newly-cut
        major-version line starts life, unproven, before being promoted
        through the same stages as everything else."""
        return self.stages[0] if self.stages else None


def branch_name(config: BranchingConfig, stage: str | None = None) -> str:
    """Computes a single branch name for the 4 configurable cases:
    major version + stage, major version only, stage only, or neither
    (a single trunk branch)."""
    parts: list[str] = []

    if config.use_major_version:
        parts.append(f"v{config.major_version}")

    if stage:
        parts.append(stage)

    if not parts:
        return config.trunk_branch

    return "-".join(parts)


def base_branch_name(config: BranchingConfig) -> str:
    """The branch feat/fix branches are always created from."""
    return branch_name(config, config.base_stage)


def entry_branch_name(config: BranchingConfig) -> str:
    """The branch a newly-cut major-version line starts as."""
    return branch_name(config, config.entry_stage)


def initial_branches(config: BranchingConfig) -> list[str]:
    """Every branch InitRepositoryUseCase should create, ordered from
    least- to most-stable. A config with no stages yields a single
    trunk branch."""
    if not config.stages:
        return [branch_name(config)]

    return [branch_name(config, stage) for stage in config.stages]


def next_major_config(config: BranchingConfig) -> BranchingConfig:
    """The BranchingConfig for the major-version line directly above this
    one — same stages/trunk naming, major_version + 1."""
    return BranchingConfig(
        use_major_version=True,
        major_version=config.major_version + 1,
        stages=config.stages,
        trunk_branch=config.trunk_branch,
    )


def stage_of_branch(config: BranchingConfig, branch: str) -> str | None:
    """The stage a branch of the current major line represents, or None
    for the base stage/trunk/major-only branch and for branches that aren't
    part of this configuration at all."""
    name = branch
    if config.use_major_version:
        prefix = f"v{config.major_version}"
        if name == prefix:
            return None
        if not name.startswith(f"{prefix}-"):
            return None
        name = name[len(prefix) + 1 :]

    return name if name in config.stages and name != config.base_stage else None


def previous_stage_branch(config: BranchingConfig, branch: str) -> str | None:
    """The branch one stage less stable than `branch` on the current major
    line — the one a missing stage branch is created from on its first
    merge. None for the entry stage or for branches outside the line."""
    branches = initial_branches(config)
    if branch not in branches:
        return None
    index = branches.index(branch)
    return branches[index - 1] if index > 0 else None


def is_work_branch(branch: str) -> bool:
    """A feat/fix/refactor/... branch, i.e. `<conventional type>/<name>`."""
    from domain.git.commit import ConventionalCommitType

    prefix, separator, _ = branch.partition("/")
    return bool(separator) and prefix in {t.value for t in ConventionalCommitType}


_STAGE_NAME = re.compile(r"^[a-z][a-z0-9_-]*$")


def parse_stages(raw: str) -> tuple[str, ...]:
    """Comma-separated stage names, least to most stable. Empty means no
    stage concept."""
    names = tuple(part.strip() for part in raw.split(",") if part.strip())
    for name in names:
        if not _STAGE_NAME.match(name):
            raise ValueError(
                f"'{name}' is not a valid stage name: use lowercase letters, "
                "digits, '-' or '_', starting with a letter."
            )
    if len(set(names)) != len(names):
        raise ValueError("stage names must be unique")
    return names
