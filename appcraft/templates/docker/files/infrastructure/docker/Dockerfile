FROM python:3.12-slim

WORKDIR /app

# Force poetry/pipenv (uv already defaults to this) to put their venv
# inside the project — a predictable path we can hand over to the
# non-root user below, instead of each manager's own default location
# outside /app (poetry: ~/.cache/pypoetry, pipenv: ~/.local/share).
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIPENV_VENV_IN_PROJECT=1

COPY . /app

# Minimal bootstrap so config/app.toml (and its `manager` key) can be
# read before we know which of poetry/pipenv/uv to hand off to —
# PackageManagerBase() below installs the manager itself, then the
# project's actual dependencies through it. include_dev_dependencies=False
# skips dev-only tooling (sphinx, flake8, black, isort, ...), which has
# no business being in a production image.
RUN pip install --no-cache-dir toml pydantic \
    && python -c "\
from infrastructure.framework.appcraft.core.package.manager.base import PackageManagerBase; \
PackageManagerBase().install_requirements(include_dev_dependencies=False)"

# Don't run the app as root.
RUN useradd --create-home appcraft && chown -R appcraft:appcraft /app
USER appcraft

ENTRYPOINT ["python", "infrastructure/docker/entrypoint.py"]
