import importlib
import os

from infrastructure.framework.appcraft.core.runner.discovery import (
    RunnerDiscovery,
)

_MAIN_RUNNERS_FOLDER = os.path.join("runners", "main")
_COMPOSE_PATH = os.path.join("infrastructure", "docker", "docker-compose.yml")
_DOCKERFILE_PATH = "infrastructure/docker/Dockerfile"
_SERVICE_METHOD = "start"


def discover_services() -> list[tuple[str, str]]:
    """Every concrete Runner under runners/main/ that exposes a `start`
    action — the convention a main runner uses to mark itself as a
    deployable service (see templates/flask/files/runners/main/flask.py's
    Flask.start). Returns (module_name, class_name) pairs, one per
    discoverable service — same discovery mechanism the web_scraping
    benchmark tool uses for runners/tools/, applied to runners/main/
    instead.
    """
    services: list[tuple[str, str]] = []

    for module_name in RunnerDiscovery.get_modules(_MAIN_RUNNERS_FOLDER):
        try:
            module = importlib.import_module(f"runners.main.{module_name}")
        except Exception:
            continue

        for app in RunnerDiscovery.get_apps(module):
            if _SERVICE_METHOD in RunnerDiscovery.get_app_runners(app):
                services.append((module_name, app.__name__))

    return services


def generate_compose_file() -> list[tuple[str, str]]:
    """(Re)writes infrastructure/docker/docker-compose.yml with one
    service per discover_services() result — build context/dockerfile
    and a `restart: unless-stopped` policy. Ports, volumes, env vars etc
    are left for the developer to add by hand, since those are
    deployment-specific and not something a Runner class exposes.

    Runs once automatically via the docker template's post_install
    (right after dependencies are installed, so RunnerDiscovery can
    actually import each runners/main module). Re-run it explicitly
    (`python run_tools docker generate_compose`) after installing a new
    runners/main template later — this is a full overwrite, so back up
    any manual edits to this file first.
    """
    services = discover_services()

    lines = ["services:"]
    for module_name, class_name in services:
        service_name = module_name.replace("_", "-")
        command_args = ", ".join(
            f'"{part}"'
            for part in (module_name, class_name, _SERVICE_METHOD)
        )
        lines.append(f"  {service_name}:")
        lines.append("    build:")
        lines.append("      context: ../..")
        lines.append(f"      dockerfile: {_DOCKERFILE_PATH}")
        lines.append(f"    command: [{command_args}]")
        lines.append("    restart: unless-stopped")

    content = "\n".join(lines) + "\n"

    with open(_COMPOSE_PATH, "w", encoding="utf-8") as file:
        file.write(content)

    return services
