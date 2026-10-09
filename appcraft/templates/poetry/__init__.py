import os
from typing import cast

import toml

from ..template_abc import TemplateABC


class PoetryTemplate(TemplateABC):
    default = True
    active = True
    exclusive_group = "package_manager"
    description = "\
Poetry template that provides a preconfigured pyproject.toml \
for dependency management."

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

        # `base` seeds the project's *first* pyproject.toml in pure PEP
        # 621 form (no package-manager-specific dialect) — this hook is
        # what turns it (or an existing pipenv/uv project being swapped)
        # into Poetry's own [tool.poetry.*] format, unconditionally, so
        # every source format goes through the same code path.
        snapshot = read_dependencies(target_dir)
        metadata = snapshot.metadata

        poetry_table: dict[str, object] = {
            "name": metadata.get("name", "Appcraft Project"),
            "version": metadata.get("version", "0.0.1"),
            "package-mode": False,
        }
        for key in ("description", "readme", "license"):
            if metadata.get(key):
                poetry_table[key] = metadata[key]
        if metadata.get("authors"):
            poetry_table["authors"] = [
                (
                    f"{author['name']} <{author['email']}>"
                    if author.get("email")
                    else author.get("name", "")
                )
                for author in metadata["authors"]
            ]
        # Poetry's own first-class fields only cover these three labels;
        # anything else (Issues, Changelog, ...) goes in the generic
        # (deprecated but still functional) [tool.poetry.urls] table
        # instead of being silently dropped.
        urls = dict(metadata.get("urls", {}))
        for label, key in (
            ("Homepage", "homepage"),
            ("Repository", "repository"),
            ("Documentation", "documentation"),
        ):
            if label in urls:
                poetry_table[key] = urls.pop(label)
        if urls:
            poetry_table["urls"] = urls
        if metadata.get("keywords"):
            poetry_table["keywords"] = metadata["keywords"]
        if metadata.get("classifiers"):
            poetry_table["classifiers"] = metadata["classifiers"]

        poetry_table["dependencies"] = {
            "python": f"^{snapshot.python_version}",
            **{
                name: constraint or "*"
                for name, constraint in snapshot.main.items()
            },
        }

        group_tables = {
            group_name: {
                "dependencies": {
                    name: constraint or "*"
                    for name, constraint in group_deps.items()
                }
            }
            for group_name, group_deps in snapshot.groups.items()
        }

        clear_dependency_sources(target_dir)

        pyproject_path = os.path.join(target_dir, "pyproject.toml")
        pyproject: dict[str, object] = {}
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r", encoding="utf-8") as file:
                pyproject = toml.load(file)

        tool = pyproject.get("tool")
        tool_table: dict[str, object] = (
            cast(dict[str, object], tool) if isinstance(tool, dict) else {}
        )

        poetry_current = tool_table.get("poetry")
        poetry_table_current: dict[str, object] = (
            cast(dict[str, object], poetry_current)
            if isinstance(poetry_current, dict)
            else {}
        )
        poetry_table_current.update(poetry_table)
        if group_tables:
            poetry_table_current["group"] = group_tables
        else:
            poetry_table_current.pop("group", None)
        if not urls:
            poetry_table_current.pop("urls", None)

        # A leftover [tool.uv] (package = false, from a prior uv swap) is
        # meaningless once Poetry owns package-mode via its own
        # package-mode = false above.
        tool_table.pop("uv", None)
        tool_table["poetry"] = poetry_table_current
        pyproject["tool"] = tool_table

        # A uv-format [project] table is now superseded by [tool.poetry];
        # keep any other top-level table as-is. [build-system] is always
        # overwritten (not setdefault): whatever format the project was
        # just converted from (base's own plain-PEP-621 default, or a
        # prior pipenv/uv swap) may have left behind a different backend
        # that can't actually build this project's layout, so Poetry's
        # own backend must win unconditionally once Poetry is active.
        pyproject.pop("project", None)
        pyproject.pop("dependency-groups", None)
        pyproject["build-system"] = {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        }

        with open(pyproject_path, "w", encoding="utf-8") as file:
            toml.dump(pyproject, file)

        set_package_manager_config(target_dir, "poetry")
