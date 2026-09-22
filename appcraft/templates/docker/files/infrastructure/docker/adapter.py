import os
import shutil
import subprocess

_COMPOSE_FILE = os.path.join("infrastructure", "docker", "docker-compose.yml")


def _compose_base_command() -> list[str]:
    """Prefers the modern `docker compose` plugin (v2); falls back to
    the standalone `docker-compose` binary (v1) if the plugin isn't
    installed — some Docker installs (a bare `docker.io` package on
    some Linux distros, older setups) only ship one or the other, and
    running the wrong one gives a confusing error (`docker` tries to
    parse `-f` as one of its own flags instead of compose's).
    """
    try:
        subprocess.run(
            ["docker", "compose", "version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return ["docker", "compose"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    if shutil.which("docker-compose"):
        return ["docker-compose"]

    raise RuntimeError(
        "Neither the `docker compose` plugin nor the standalone "
        "`docker-compose` binary was found. Install Docker Compose: "
        "https://docs.docker.com/compose/install/"
    )


class DockerAdapter:
    """Thin wrapper around the compose CLI, always pointed at
    infrastructure/docker/docker-compose.yml via `-f` — so callers don't
    need to `cd` there first, regardless of where they run `python
    run_tools` from.
    """

    def build(self, service: str | None = None) -> None:
        command = _compose_base_command() + ["-f", _COMPOSE_FILE, "build"]
        if service:
            command.append(service)
        subprocess.check_call(command)

    def up(self, service: str | None = None) -> None:
        command = _compose_base_command() + ["-f", _COMPOSE_FILE, "up"]
        if service:
            command.append(service)
        subprocess.check_call(command)

    def down(self) -> None:
        command = _compose_base_command() + ["-f", _COMPOSE_FILE, "down"]
        subprocess.check_call(command)
