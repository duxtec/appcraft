from domain.git.branching import BranchingConfig
from infrastructure.core.config import Config
from infrastructure.git.toml_edit import set_value

_GIT_CONFIG_PATH = "config/git.toml"


def get_branching_config() -> BranchingConfig:
    config = Config().get("git")

    return BranchingConfig(
        use_major_version=bool(config.get("use_major_version", False)),
        major_version=int(config.get("major_version", 0)),
        stages=tuple(config.get("stages", [])),
        trunk_branch=str(config.get("trunk_branch", "main")),
    )


def is_configured() -> bool:
    return bool(Config().get("git").get("configured", False))


def write_branching_config(config: BranchingConfig) -> None:
    """Stores the chosen strategy and marks the setup as done. Values are
    written in place, so the file's comments stay."""
    with open(_GIT_CONFIG_PATH, "r") as file:
        text = file.read()

    text = set_value(text, "use_major_version", config.use_major_version)
    text = set_value(text, "major_version", config.major_version)
    text = set_value(text, "stages", list(config.stages))
    text = set_value(text, "trunk_branch", config.trunk_branch)
    text = set_value(text, "configured", True)

    with open(_GIT_CONFIG_PATH, "w") as file:
        file.write(text)


def write_major_version(value: int) -> None:
    # Config() is read-only, so the value is written in place to keep the
    # file's comments.
    with open(_GIT_CONFIG_PATH, "r") as file:
        text = file.read()

    with open(_GIT_CONFIG_PATH, "w") as file:
        file.write(set_value(text, "major_version", value))
