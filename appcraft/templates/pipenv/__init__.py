import os

import toml

from ..template_abc import TemplateABC


class PipenvTemplate(TemplateABC):
    active = True
    exclusive_group = "package_manager"
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
        from appcraft.utils.dependency_convert import (  # pyright: ignore[reportMissingImports, reportMissingTypeStubs]
            clear_dependency_sources,
            read_dependencies,
            set_package_manager_config,
        )

        target_dir = target_dir or os.getcwd()

        snapshot = read_dependencies(target_dir)

        # Pipfile has no equivalent of Poetry's/uv's named, installed-by-
        # default-but-individually-excludable groups: a bare `pipenv
        # install` only ever installs [packages] — [dev-packages] and
        # any custom category need an explicit --dev/--categories flag,
        # confirmed empirically. So every group ("dev" included)
        # collapses into [packages] here, to keep a bare `pipenv
        # install`'s default behavior matching poetry/uv's (everything
        # installed) — at the cost of Pipenv losing the ability to
        # exclude one group for a lean/production install the way
        # `poetry install --without <group>`/`uv sync --no-group <group>`
        # can. [dev-packages] is always left empty rather than
        # repurposed, since nothing reads it back as meaningfully
        # distinct from [packages] once this flattening happens.
        all_packages: dict[str, str] = dict(snapshot.main)
        for group_deps in snapshot.groups.values():
            all_packages.update(group_deps)

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
                for name, constraint in all_packages.items()
            },
            "dev-packages": {},
        }

        clear_dependency_sources(target_dir)

        with open(
            os.path.join(target_dir, "Pipfile"), "w", encoding="utf-8"
        ) as file:
            toml.dump(pipfile, file)

        set_package_manager_config(target_dir, "pipenv")
