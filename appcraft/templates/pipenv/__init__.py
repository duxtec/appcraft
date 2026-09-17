import os

import toml

from ..template_abc import TemplateABC


class PipenvTemplate(TemplateABC):
    active = True
    exclusive_group = "package_manager"
    dependencies = ["poetry"]
    description = "\
Pipenv Template switches the project's dependency management to Pipenv. \
It reads whatever dependencies the project currently has — from Poetry, \
uv, or an existing Pipfile — and writes them as a Pipfile, replacing \
whichever format was previously in use."

    @classmethod
    def pre_install(cls, target_dir: str | None = None) -> None:
        # Local import: appcraft.utils.dependency_convert lives in the CLI
        # package, which only exists in the dev environment — never in a
        # generated project. This __init__.py is copied into every
        # generated project as the is_installed() marker (see
        # TemplateABC.install(), which lazily imports
        # appcraft.utils.template.adder the same way), so the import must
        # stay inside pre_install (only ever called from the CLI) instead
        # of at module level, or importing this marker to check
        # is_installed() would crash in every generated project. Only
        # resolves for pyright when the appcraft dev dependency (added by
        # this template's own pyproject.toml fragment) is installed.
        from appcraft.utils.dependency_convert import (  # pyright: ignore[reportMissingImports]
            clear_dependency_sources,
            read_dependencies,
            set_package_manager_config,
        )

        target_dir = target_dir or os.getcwd()

        snapshot = read_dependencies(target_dir)

        dev_deps: dict[str, str] = {}
        for group_deps in snapshot.groups.values():
            dev_deps.update(group_deps)

        pipfile = {
            "source": [
                {
                    "url": "https://pypi.org/simple",
                    "verify_ssl": True,
                    "name": "pypi",
                }
            ],
            "requires": {"python_version": snapshot.python_version},
            "packages": {
                name: constraint or "*"
                for name, constraint in snapshot.main.items()
            },
            "dev-packages": {
                name: constraint or "*"
                for name, constraint in dev_deps.items()
            },
        }

        clear_dependency_sources(target_dir)

        with open(
            os.path.join(target_dir, "Pipfile"), "w", encoding="utf-8"
        ) as file:
            toml.dump(pipfile, file)

        set_package_manager_config(target_dir, "pipenv")
