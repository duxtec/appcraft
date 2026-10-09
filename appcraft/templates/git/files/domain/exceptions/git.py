class GitError(RuntimeError):
    pass


class NotAGitRepositoryError(GitError):
    def __init__(self, *args: object) -> None:
        if not args:
            args = ("This directory is not a git repository.",)
        super().__init__(*args)


class NotAReleaseBranchError(GitError):
    def __init__(self, branch: str, *args: object) -> None:
        if not args:
            args = (
                f"'{branch}' is not a stage branch of the current major "
                "version — releases must be cut from one of them.",
            )
        super().__init__(*args)


class FirstReleaseNotEntryError(GitError):
    def __init__(
        self, major: int, entry_stage: str | None, entry_label: str | None, *args: object
    ) -> None:
        if not args:
            where = (
                f"the '{entry_stage}' stage (the least stable one)"
                if entry_stage
                else "the least stable stage"
            )
            first = f"{major}.0.0{entry_label or ''}1"
            args = (
                f"The first release of major version {major} must be cut from "
                f"{where}, as {first}.",
            )
        super().__init__(*args)
