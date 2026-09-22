from infrastructure.framework.appcraft.core.package.manager.base import (
    PackageManagerBase,
)

from ..template_abc import TemplateABC


class DockerTemplate(TemplateABC):
    active = True
    description = "\
Docker Template containerizes the application. It ships a single Dockerfile \
that installs dependencies through whichever package manager the project \
is currently using (Poetry, Pipenv or uv — no hardcoded assumption), and a \
docker-compose.yml generated automatically from every runners/main Runner \
that exposes a `start` action, one service per deployable entry point. \
Re-run `python run_tools docker generate_compose` after installing a new \
runners/main template (e.g. a future FastAPI or GUI template) to pick it \
up — the file isn't regenerated silently on every unrelated template \
install, so manual edits (ports, volumes, env vars) aren't clobbered."

    @classmethod
    def post_install(cls, target_dir: str | None = None) -> None:
        # Unlike e.g. git's post_install, this has to import every
        # runners/main module to discover services — including their
        # third-party dependencies (flask, etc), which only exist inside
        # the project's own package-manager environment. Bare `python`
        # (the CLI's own interpreter) doesn't have those installed, so
        # this must go through PackageManagerBase().run_command() (the
        # same `poetry run`/`pipenv run`/`uv run` wrapper a developer
        # would use manually) instead of shelling out directly. It
        # already handles/reports a failing subprocess itself.
        PackageManagerBase().run_command(
            ["python", "run_tools", "docker", "generate_compose"]
        )
