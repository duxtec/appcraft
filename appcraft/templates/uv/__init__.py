import os
from typing import cast

import toml

from ..template_abc import TemplateABC


class UvTemplate(TemplateABC):
    active = True
    exclusive_group = "package_manager"
    description = "\
uv Template switches the project's dependency management to uv. It reads \
whatever dependencies the project currently has — from Poetry, Pipenv, or \
an existing uv pyproject.toml — and writes them as native PEP 621 \
[project] / [dependency-groups] tables, replacing whichever format was \
previously in use."

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
        metadata = snapshot.metadata

        project: dict[str, object] = {
            "name": cls._normalize_name(
                metadata.get("name", "appcraft-project")
            ),
            "version": metadata.get("version", "0.0.1"),
            "requires-python": f">={snapshot.python_version}",
            "dependencies": cls._pep508_list(snapshot.main),
        }

        if metadata.get("description"):
            project["description"] = metadata["description"]
        if metadata.get("authors"):
            project["authors"] = metadata["authors"]
        if metadata.get("readme"):
            project["readme"] = metadata["readme"]
        if metadata.get("license"):
            # Plain PEP 639 SPDX string, not the legacy {text = ...}
            # table — metadata["license"] is always already just an
            # SPDX expression string (e.g. "MIT"), never arbitrary
            # free-text, regardless of which format it was read from.
            project["license"] = metadata["license"]
        if metadata.get("license_files"):
            project["license-files"] = metadata["license_files"]
        if metadata.get("keywords"):
            project["keywords"] = metadata["keywords"]
        if metadata.get("classifiers"):
            project["classifiers"] = metadata["classifiers"]

        if metadata.get("urls"):
            project["urls"] = dict(metadata["urls"])

        dependency_groups = {
            group_name: cls._pep508_list(group_deps)
            for group_name, group_deps in snapshot.groups.items()
        }

        clear_dependency_sources(target_dir)

        pyproject_path = os.path.join(target_dir, "pyproject.toml")
        pyproject: dict[str, object] = {}
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r", encoding="utf-8") as file:
                pyproject = toml.load(file)

        # Poetry's own metadata table is now superseded by [project];
        # keep any other [tool.*] table as-is.
        tool = pyproject.get("tool")
        tool_table: dict[str, object] = (
            cast(dict[str, object], tool) if isinstance(tool, dict) else {}
        )
        tool_table.pop("poetry", None)
        # Mirrors Poetry's own package-mode = false: this project's
        # top-level layout (domain/, application/, infrastructure/, ...)
        # is a Clean Architecture app, not an installable distribution,
        # so uv must never try to build/install it as its own package —
        # that fails outright (setuptools' auto-discovery sees multiple
        # top-level packages and refuses to build).
        #
        # default-groups must be set explicitly (and must list every
        # group, "dev" included): `uv sync` only auto-installs the "dev"
        # group by its own built-in convention, and setting
        # default-groups at all *replaces* that implicit default rather
        # than adding to it — confirmed empirically (an explicit
        # default-groups missing "dev" silently stops installing it).
        # Mirrors Poetry's groups, which install by default unless
        # marked optional = true (never done here), so `(poetry|uv)
        # install`'s default behavior matches regardless of which
        # manager is active; `uv sync --no-group <name>` (or Poetry's
        # `--without <name>`) excludes one, e.g. for a lean production
        # image.
        tool_table["uv"] = {
            "package": False,
            "default-groups": list(dependency_groups.keys()),
        }
        pyproject["tool"] = tool_table

        # A leftover [build-system] (from base's own default, or a prior
        # poetry/pipenv swap) is irrelevant once package = false — uv
        # never invokes it.
        pyproject.pop("build-system", None)

        pyproject["project"] = project
        if dependency_groups:
            pyproject["dependency-groups"] = dependency_groups
        elif "dependency-groups" in pyproject:
            del pyproject["dependency-groups"]

        with open(pyproject_path, "w", encoding="utf-8") as file:
            toml.dump(pyproject, file)

        set_package_manager_config(target_dir, "uv")

    @staticmethod
    def _pep508_list(deps: dict[str, str]) -> list[str]:
        return [name + constraint for name, constraint in deps.items()]

    @staticmethod
    def _normalize_name(name: str) -> str:
        return name.strip().lower().replace(" ", "-").replace("_", "-")
