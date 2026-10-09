_interactive = True


class MissingInputError(RuntimeError):
    pass


class InvalidInputError(ValueError):
    pass


def set_interactive(value: bool) -> None:
    global _interactive
    _interactive = value


def is_interactive() -> bool:
    return _interactive


def read_input(prompt: str, argument: str) -> str:
    """Asks the user, but only in an interactive run. A command line run
    never waits for input: a missing value is an error naming the argument
    to pass instead."""
    if not _interactive:
        raise MissingInputError(
            f"Missing argument '{argument}'. Pass it as {argument}=<value>."
        )
    return input(prompt)
