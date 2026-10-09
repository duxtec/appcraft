import importlib
import re
from dataclasses import replace
from typing import Protocol

from application.use_cases.git.create_feature_branch import (
    CreateFeatureBranchInput,
    CreateFeatureBranchUseCase,
)
from application.use_cases.git.create_release import CreateReleaseUseCase
from application.use_cases.git.delete_branches import DeleteBranchesUseCase
from application.use_cases.git.list_cleanup_branches import (
    ListCleanupBranchesUseCase,
)
from application.use_cases.git.list_unreleased_commits import (
    ListUnreleasedCommitsUseCase,
)
from application.use_cases.git.cut_major_version import (
    CutMajorVersionUseCase,
)
from application.use_cases.git.detect_next_version import (
    DetectNextInput,
    DetectNextVersionUseCase,
)
from application.use_cases.git.init_repository import InitRepositoryUseCase
from application.use_cases.git.merge_branch import (
    MergeBranchInput,
    MergeBranchUseCase,
)
from domain.exceptions.git import (
    FirstReleaseNotEntryError,
    NotAReleaseBranchError,
)
from domain.git.branching import (
    BranchingConfig,
    base_branch_name,
    entry_branch_name,
    initial_branches,
    parse_stages,
    previous_stage_branch,
    stage_of_branch,
)
from domain.git.changelog import render_changelog
from domain.git.commit import ConventionalCommit, ConventionalCommitType
from domain.git.version import PRERELEASE_LABELS, SemVer
from infrastructure.core.runner import Runner
from infrastructure.core.runner.mode import (
    InvalidInputError,
    is_interactive,
    read_input,
)
from infrastructure.git.adapter import GitAdapter
from infrastructure.git.config import (
    get_branching_config,
    is_configured,
    write_branching_config,
    write_major_version,
)
from infrastructure.git.hooks import install_commit_msg_hook
from infrastructure.git.version_file import write_pyproject_version
from presentation.cli.git import GitCLIPresentation


def _apply_overrides(
    defaults: BranchingConfig, overrides: dict[str, str]
) -> BranchingConfig:
    values: dict[str, object] = {}
    if "use_major_version" in overrides:
        values["use_major_version"] = _parse_bool(overrides["use_major_version"])
    if "major_version" in overrides:
        values["major_version"] = _parse_major(overrides["major_version"])
    if "stages" in overrides:
        raw = overrides["stages"].strip()
        values["stages"] = () if raw.lower() == "none" else parse_stages(raw)
    if "trunk_branch" in overrides:
        values["trunk_branch"] = overrides["trunk_branch"]
    return replace(defaults, **values)


def _parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in ("true", "yes", "y", "1"):
        return True
    if value in ("false", "no", "n", "0"):
        return False
    raise InvalidInputError(f"'{raw}' is not a boolean: use true or false.")


def _parse_major(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"'{raw}' is not a whole number.") from None
    if value < 0:
        raise ValueError("The major version can't be negative.")
    return value


class _RemoteHost(Protocol):
    def create_release(
        self, tag: str, title: str, notes: str, prerelease: bool
    ) -> str: ...

    def get_default_branch(self) -> str | None: ...

    def set_default_branch(self, name: str) -> None: ...


def _get_remote_repository_adapter() -> _RemoteHost | None:
    # Checked at runtime via is_installed() (not a hard dependency) since
    # `git` is standalone and must work with no hosting platform installed
    # at all — same marker mechanism flask/locales use for their siblings.
    try:
        template_module = importlib.import_module(
            "infrastructure.framework.appcraft.templates.remote_repository"
        )
        remote_repository_template = template_module.RemoteRepositoryTemplate

        if not remote_repository_template.is_installed():
            return None

        provider_module = importlib.import_module(
            "infrastructure.remote_repository.provider"
        )
        return provider_module.get_default_remote_repository_adapter()
    except Exception:
        return None


def _confirmed(question: str) -> bool:
    if not is_interactive():
        return True
    return read_input(f"{question} (y/N): ", "interactive").strip().lower() in ("y", "yes")


def _major_of_branch(branch: str | None) -> int:
    match = re.match(r"^v(\d+)", branch or "")
    return int(match.group(1)) if match else 0


def _prepend_to_file(path: str, text: str) -> None:
    try:
        with open(path, "r") as file:
            existing = file.read()
    except FileNotFoundError:
        existing = ""

    with open(path, "w") as file:
        file.write(text + "\n" + existing)


class Git(Runner):
    def __init__(self) -> None:
        self.git = GitAdapter()
        self.presentation = GitCLIPresentation()

    @Runner.runner
    def init(
        self,
        use_major_version: str | None = None,
        major_version: str | None = None,
        stages: str | None = None,
        trunk_branch: str | None = None,
    ):
        overrides = {
            key: value
            for key, value in {
                "use_major_version": use_major_version,
                "major_version": major_version,
                "stages": stages,
                "trunk_branch": trunk_branch,
            }.items()
            if value is not None
        }

        if is_configured():
            if overrides:
                raise InvalidInputError(self.presentation.setup_already_done_message())
            config = get_branching_config()
        else:
            try:
                config = self._setup_config(overrides)
            except ValueError as error:
                raise InvalidInputError(str(error)) from error
            write_branching_config(config)

        InitRepositoryUseCase(self.git).execute(config)
        install_commit_msg_hook()

    def _setup_config(self, overrides: dict[str, str]) -> BranchingConfig:
        defaults = get_branching_config()
        if overrides:
            return _apply_overrides(defaults, overrides)
        if is_interactive():
            return self.presentation.ask_setup(defaults)
        return defaults

    @Runner.runner
    def start(self, kind: str, name: str):
        valid_kinds = [commit_type.value for commit_type in ConventionalCommitType]
        if kind not in valid_kinds:
            raise InvalidInputError(
                f"'{kind}' is not a Conventional Commits type. Use one of: "
                + ", ".join(valid_kinds)
            )

        config = get_branching_config()
        base_branch = base_branch_name(config)

        branch = CreateFeatureBranchUseCase(self.git).execute(
            CreateFeatureBranchInput(
                kind=kind, name=name, base_branch=base_branch
            )
        )
        self.presentation.Printer.branch_created(branch, base_branch)

    @Runner.runner
    def merge(self, source: str, target: str):
        if not self.git.branch_exists(target):
            source_stage = previous_stage_branch(get_branching_config(), target)
            if source_stage is not None:
                self.git.create_branch(target, source=source_stage)
                self.presentation.Printer.stage_created(target, source_stage)

        config = get_branching_config()

        if config.use_major_version:
            incoming = self.git.commits_between(target, source)
            is_breaking = any(
                ConventionalCommit.parse(message).is_breaking
                for message in incoming
            )

            top_config = replace(config, major_version=self._top_major(config))
            if is_breaking and config.major_version < top_config.major_version:
                self.presentation.Printer.higher_major_exists(
                    target, base_branch_name(top_config)
                )
                return
            if is_breaking and self._has_stable_release(top_config):
                new_config = self._cut_next_major(top_config)
                new_target = entry_branch_name(new_config)
                self.presentation.Printer.redirected_to_major(
                    target, new_target
                )
                target = new_target

        MergeBranchUseCase(self.git).execute(
            MergeBranchInput(source=source, target=target)
        )
        self.presentation.Printer.merged(source, target)

    @Runner.runner(pause=True)
    def detect_version(self):
        try:
            version = self._next_version()
        except (NotAReleaseBranchError, FirstReleaseNotEntryError) as e:
            self.presentation.Printer.release_not_on_stage(str(e))
            return None
        if version is None:
            self.presentation.Printer.no_releasable_changes()
            return None

        self.presentation.Printer.next_version(version)
        return version

    @Runner.runner
    def release(self):
        try:
            version = self._next_version()
        except (NotAReleaseBranchError, FirstReleaseNotEntryError) as e:
            self.presentation.Printer.release_not_on_stage(str(e))
            return
        if version is None:
            self.presentation.Printer.no_releasable_changes()
            return

        self.presentation.Printer.next_version(version)
        if not _confirmed(f"Release v{version}?"):
            return

        write_pyproject_version(str(version))
        self.git.add_all()
        if self.git.has_changes():
            self.git.commit(f"chore(release): v{version}")
            self.git.push(self.git.current_branch())

        tag = CreateReleaseUseCase(self.git).execute(version)
        self.presentation.Printer.released(tag)

        remote_adapter = _get_remote_repository_adapter()
        if remote_adapter is not None and self.git.get_remote() is not None:
            if not version.is_prerelease:
                self._promote_default_branch(remote_adapter, version)
            try:
                remote_adapter.create_release(
                    tag=tag,
                    title=tag,
                    notes=f"Release {tag}",
                    prerelease=version.is_prerelease,
                )
            except Exception as e:
                # The git tag/commit above already succeeded — a failure
                # creating the platform release (e.g. not authenticated)
                # shouldn't look like the whole release failed.
                self.presentation.Printer.platform_release_error(str(e))

    def _top_major(self, config: BranchingConfig) -> int:
        majors = [
            int(match.group(1))
            for branch in self.git.list_branches()
            if (match := re.match(r"^v(\d+)", branch))
        ]
        return max(majors, default=config.major_version)

    def _has_stable_release(self, config: BranchingConfig) -> bool:
        """A new major line only starts once the current one has shipped a
        stable release (a tag without a pre-release label reachable from its
        base branch)."""
        base = base_branch_name(config)
        for tag in self.git.reachable_tags(base):
            try:
                version = SemVer.parse(tag)
            except ValueError:
                continue
            if not version.is_prerelease and version.major == config.major_version:
                return True
        return False

    def _cut_next_major(self, config: BranchingConfig) -> BranchingConfig:
        new_config = CutMajorVersionUseCase(self.git).execute(config)
        self.git.checkout(entry_branch_name(new_config))
        if get_branching_config().major_version != new_config.major_version:
            write_major_version(new_config.major_version)
            self.git.add_all()
            self.git.commit(
                "chore(git): bump major_version to "
                f"{new_config.major_version}"
            )
        return new_config

    def _promote_default_branch(
        self, remote_adapter: _RemoteHost, version: SemVer
    ) -> None:
        """The repository's default branch follows the highest major version
        with a stable release, so after 1.0.0 is cut from v1-main, GitHub's
        default branch becomes v1-main."""
        branch = self.git.current_branch()
        try:
            current_default = remote_adapter.get_default_branch()
        except Exception as e:
            self.presentation.Printer.default_branch_error(str(e))
            return
        if current_default == branch or version.major <= _major_of_branch(
            current_default
        ):
            return

        try:
            self.git.push(branch)
            remote_adapter.set_default_branch(branch)
        except Exception as e:
            self.presentation.Printer.default_branch_error(str(e))
            return
        self.presentation.Printer.default_branch_changed(
            current_default, branch
        )

    def _next_version(self) -> SemVer | None:
        label = self._release_label()
        config = get_branching_config()
        refs = tuple(
            branch for branch in initial_branches(config) if self.git.branch_exists(branch)
        ) or ("HEAD",)
        line_major = config.major_version if config.use_major_version else None
        return DetectNextVersionUseCase(self.git).execute(
            DetectNextInput(
                label=label,
                refs=refs,
                line_major=line_major,
                entry_stage=config.entry_stage,
                entry_label=PRERELEASE_LABELS.get(config.entry_stage or ""),
            )
        )

    def _release_label(self) -> str | None:
        """The pre-release label the current branch produces: None on the
        base stage (stable release), 'a'/'b'/'rc' on alpha/beta/rc."""
        config = get_branching_config()
        branch = self.git.current_branch()

        if branch not in initial_branches(config):
            raise NotAReleaseBranchError(branch)

        stage = stage_of_branch(config, branch)
        if stage is None:
            return None
        if stage not in PRERELEASE_LABELS:
            raise NotAReleaseBranchError(branch)
        return PRERELEASE_LABELS[stage]

    @Runner.runner
    def set_remote(self, url: str | None = None):
        self.git.set_remote(url)

    @Runner.runner
    def new_major(self):
        config = get_branching_config()
        if not config.use_major_version:
            self.presentation.Printer.major_not_enabled()
            return
        top_config = replace(config, major_version=self._top_major(config))
        if not self._has_stable_release(top_config):
            self.presentation.Printer.major_blocked(top_config.major_version)
            return

        new_config = self._cut_next_major(top_config)
        self.presentation.Printer.major_cut(
            entry_branch_name(new_config), new_config.major_version
        )

    @Runner.runner(pause=True)
    def changelog(self, output: str | None = None):
        config = get_branching_config()
        refs = tuple(
            branch for branch in initial_branches(config) if self.git.branch_exists(branch)
        ) or ("HEAD",)
        unreleased = ListUnreleasedCommitsUseCase(self.git).execute(refs)
        title = (
            f"Unreleased changes since {unreleased.latest}"
            if unreleased.latest
            else "Unreleased changes"
        )
        text = render_changelog(unreleased.commits, title)
        print(text)

        if output is not None:
            _prepend_to_file(output, text)
            self.presentation.Printer.changelog_written(output)

    @Runner.runner
    def cleanup(self):
        stable = base_branch_name(get_branching_config())
        if not self.git.branch_exists(stable):
            self.presentation.Printer.nothing_to_clean()
            return

        candidates = ListCleanupBranchesUseCase(self.git).execute(stable)
        if not candidates.local and not candidates.remote:
            self.presentation.Printer.nothing_to_clean()
            return

        if candidates.local:
            print(f"Local branches merged into '{stable}':")
            for branch in candidates.local:
                print(f"  - {branch}")
        if candidates.remote:
            print(f"Remote branches on origin merged into '{stable}':")
            for branch in candidates.remote:
                print(f"  - origin/{branch}")
        if not _confirmed("Delete them?"):
            return

        DeleteBranchesUseCase(self.git).execute(candidates)
        self.presentation.Printer.branches_deleted(
            len(candidates.local) + len(candidates.remote)
        )
