class RemoteRepositoryError(RuntimeError):
    pass


class RepositoryNotFoundError(RemoteRepositoryError):
    def __init__(self, name: str, *args: object) -> None:
        if not args:
            args = (f"Repository '{name}' not found.",)
        super().__init__(*args)


class PlatformCLINotAvailableError(RemoteRepositoryError):
    def __init__(self, cli_name: str, *args: object) -> None:
        if not args:
            args = (
                f"'{cli_name}' is not installed. Install it and try again.",
            )
        super().__init__(*args)


class PlatformNotAuthenticatedError(RemoteRepositoryError):
    def __init__(self, cli_name: str, *args: object) -> None:
        if not args:
            args = (
                f"Not authenticated with '{cli_name}'. "
                f"Run '{cli_name} auth login'.",
            )
        super().__init__(*args)
