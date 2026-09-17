import os

import toml

from ..template_abc import TemplateABC


class UvTemplate(TemplateABC):
    active = True
    exclusive_group = "package_manager"
    dependencies = ["poetry"]
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
        from appcraft.utils.dependency_convert import (  # pyright: ignore[reportMissingImports]
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
            project["license"] = {"text": metadata["license"]}
        if metadata.get("keywords"):
            project["keywords"] = metadata["keywords"]
        if metadata.get("classifiers"):
            project["classifiers"] = metadata["classifiers"]

        urls = {
            label: metadata[key]
            for key, label in (
                ("homepage", "Homepage"),
                ("repository", "Repository"),
                ("documentation", "Documentation"),
            )
            if metadata.get(key)
        }
        if urls:
            project["urls"] = urls

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
        # keep any other [tool.*] table / [build-system] as-is.
        tool = pyproject.get("tool")
        if isinstance(tool, dict) and "poetry" in tool:
            del tool["poetry"]
            if not tool:
                del pyproject["tool"]

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
