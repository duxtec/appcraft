import os
import sys

# Running this as `python infrastructure/docker/entrypoint.py` (the
# Dockerfile's ENTRYPOINT) puts this file's own directory on sys.path,
# not the project root (WORKDIR /app) — so `infrastructure.framework...`
# doesn't resolve unless the project root is added explicitly first.
sys.path.insert(0, os.getcwd())

from infrastructure.framework.appcraft.core.package.manager.base import (  # noqa: E402,E501
    PackageManagerBase,
)

# Forwards whatever the image was told to run (a docker-compose service's
# `command:`, e.g. ["flask", "Flask", "start"]) to `python run`, through
# whichever package manager the project is actually using — the same
# PackageManagerBase().run_command() wrapper `poetry run`/`pipenv run`/
# `uv run` a local dev environment already goes through, so this doesn't
# need to know or care which of the three is active.
if __name__ == "__main__":
    PackageManagerBase().run_command(["python", "run", *sys.argv[1:]])
