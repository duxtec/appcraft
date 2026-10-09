import sys

from infrastructure.core.package.manager import PackageManagerBase

from ..template_abc import TemplateABC


class GitTemplate(TemplateABC):
    active = True
    description = "\
Git Template sets up a Git repository for version control. It includes \
pre-configured files like `.gitignore` and a default repository structure, \
a configurable branching strategy, Conventional Commits, and automatic \
next-version detection, ensuring that the project is ready to be tracked \
and managed with Git."

    @classmethod
    def post_install(cls, target_dir: str | None = None) -> None:
        command = ["python", "tools", "git", "init"]
        if not sys.stdin.isatty():
            command.append("interactive=false")
        # Not subprocess.check_call(command) directly: "python" there
        # would resolve to whichever interpreter is running appcraft
        # itself, not this generated project's own (Poetry/Pipenv/uv)
        # venv — so a dependency only installed in the generated
        # project, e.g. structlog from the logs template, would raise
        # ModuleNotFoundError the moment this subprocess imports
        # anything that needs it. PackageManagerBase().run_command()
        # already wraps the call correctly per active manager (e.g.
        # `poetry run python ...`), so every other direct-subprocess
        # call in the framework goes through it instead of raw
        # subprocess.check_call — this one was the one exception.
        PackageManagerBase().run_command(command)
