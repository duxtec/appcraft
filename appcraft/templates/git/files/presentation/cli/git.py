from domain.git.branching import BranchingConfig, parse_stages
from infrastructure.core.runner.mode import read_input
from domain.git.version import SemVer
from infrastructure.utils.component_printer import (
    ComponentPrinter,
)


class GitCLIPresentation:
    @staticmethod
    def setup_already_done_message() -> str:
        return (
            "The branching strategy is already set up. Edit config/git.toml by "
            "hand to change it, then create the branches you need."
        )

    class Printer(ComponentPrinter):
        domain = "git"

        @classmethod
        def setup_already_done(cls):
            cls.error(
                "The branching strategy is already set up. Edit "
                "config/git.toml by hand to change it, then create the "
                "branches you need."
            )

        @classmethod
        def invalid_setup_value(cls, message: str):
            cls.error(message)

        @classmethod
        def branch_created(cls, branch: str, source: str):
            cls.success(f"Branch '{branch}' created from '{source}'.")

        @classmethod
        def merged(cls, source: str, target: str):
            cls.success(f"Merged '{source}' into '{target}'.")

        @classmethod
        def redirected_to_major(cls, original_target: str, new_target: str):
            cls.warning(
                f"'{original_target}' contains breaking changes — "
                f"redirected the merge to '{new_target}' instead. "
                f"'{original_target}' was not touched."
            )

        @classmethod
        def no_releasable_changes(cls):
            cls.warning(
                "No feat/fix/breaking commits since the last tag — "
                "nothing to release."
            )

        @classmethod
        def next_version(cls, version: SemVer):
            cls.title("Next version", end=": ")
            cls.success(str(version))

        @classmethod
        def release_not_on_stage(cls, message: str):
            cls.error(message)

        @classmethod
        def invalid_branch_kind(cls, kind: str, valid_kinds: list[str]):
            cls.error(
                f"'{kind}' is not a Conventional Commits type. Use one of: "
                + ", ".join(valid_kinds)
            )

        @classmethod
        def stage_created(cls, branch: str, source: str):
            cls.info(f"Stage branch '{branch}' created from '{source}'.")

        @classmethod
        def default_branch_changed(cls, previous: str | None, branch: str):
            cls.success(
                f"Default branch changed from '{previous}' to '{branch}'."
            )

        @classmethod
        def default_branch_error(cls, reason: str):
            cls.warning(f"Could not update the default branch: {reason}")

        @classmethod
        def major_not_enabled(cls):
            cls.error(
                "Major-version branches are disabled: set "
                "use_major_version = true in config/git.toml first."
            )

        @classmethod
        def major_blocked(cls, major_version: int):
            cls.error(
                f"Major version {major_version} has no stable release yet. "
                "A new major line only starts after the current one ships "
                f"a stable {major_version}.x.y release."
            )

        @classmethod
        def higher_major_exists(cls, target: str, higher: str):
            cls.error(
                f"'{target}' contains breaking changes, but a higher major "
                f"line already exists ('{higher}'). A breaking change can only "
                "start the next major, so this merge was refused. Merge it into "
                "the line that is currently the newest, or change the commit."
            )

        @classmethod
        def major_cut(cls, entry_branch: str, major_version: int):
            cls.success(
                f"Major version {major_version} line cut: '{entry_branch}' "
                "is ready. Promote work into it with `merge`."
            )

        @classmethod
        def nothing_to_clean(cls):
            cls.info("No merged feat/fix branches to clean up.")

        @classmethod
        def branches_deleted(cls, count: int):
            cls.success(f"Deleted {count} merged branch(es).")

        @classmethod
        def changelog_written(cls, path: str):
            cls.success(f"Changelog section written to '{path}'.")

        @classmethod
        def released(cls, tag: str):
            cls.success(f"Released '{tag}'.")

        @classmethod
        def platform_release_error(cls, reason: str):
            cls.warning(
                f"Tag pushed, but the platform release failed: {reason}"
            )

    def ask_setup(self, defaults: BranchingConfig) -> BranchingConfig:
        print("Set up the branching strategy (press Enter to keep the default).")
        use_major_version = _ask_bool(
            "Use major-version branches (v0-..., v1-...)?",
            defaults.use_major_version,
        )
        major_version = defaults.major_version
        if use_major_version:
            major_version = _ask_int(
                "Current major version", defaults.major_version
            )
        stages = _ask_stages(defaults.stages)
        trunk_branch = defaults.trunk_branch
        if not stages:
            trunk_branch = _ask_text(
                "Name of the single branch", defaults.trunk_branch
            )
        return BranchingConfig(
            use_major_version=use_major_version,
            major_version=major_version,
            stages=stages,
            trunk_branch=trunk_branch,
        )


def _ask_text(question: str, default: str) -> str:
    answer = read_input(f"{question} [{default}]: ", question).strip()
    return answer or default


def _ask_bool(question: str, default: bool) -> bool:
    shown = "Y/n" if default else "y/N"
    while True:
        answer = read_input(f"{question} [{shown}]: ", question).strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes", "true", "1"):
            return True
        if answer in ("n", "no", "false", "0"):
            return False
        print("Please answer y or n.")


def _ask_int(question: str, default: int) -> int:
    while True:
        answer = read_input(f"{question} [{default}]: ", question).strip()
        if not answer:
            return default
        try:
            value = int(answer)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value >= 0:
            return value
        print("The major version can't be negative.")


def _ask_stages(default: tuple[str, ...]) -> tuple[str, ...]:
    shown = ",".join(default) or "none"
    while True:
        answer = read_input(
            "Stages, least to most stable, comma separated "
            f"('none' for no stages) [{shown}]: ",
            "stages",
        ).strip()
        if not answer:
            return default
        if answer.lower() == "none":
            return ()
        try:
            return parse_stages(answer)
        except ValueError as error:
            print(error)
