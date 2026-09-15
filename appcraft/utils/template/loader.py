import os
from os import listdir
from pathlib import Path
from typing import Type

from appcraft.templates.template_abc import TemplateABC
from appcraft.utils import ImportManager
from appcraft.utils.exceptions import (
    TemplateConflictError,
    TemplateInactiveError,
    TemplateNotFoundError,
    TemplateNotStandaloneError,
)


class TemplateLoader:
    def __init__(self, get_inactives: bool = False):
        self.template_dir = Path(__file__).resolve().parents[2] / "templates"
        self.templates: list[Type[TemplateABC]] = []
        self.template_names: list[str] = []
        self.default_templates: list[Type[TemplateABC]] = []
        self.default_template_names: list[str] = []
        self.get_inactives = get_inactives

        self._load_templates()

    def _load_templates(self) -> None:
        for dir in listdir(self.template_dir):
            if not os.path.isdir(os.path.join(self.template_dir, dir)):
                continue

            im = ImportManager("appcraft.templates")

            try:
                attributes = im.get_module_attributes(dir)

                for _, attribute in attributes.items():
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, TemplateABC)
                        and attribute is not TemplateABC
                    ):
                        template = attribute

                        if template.active or self.get_inactives:
                            self.templates.append(template)
                            self.template_names.append(template.name)

                            if template.default:
                                self.default_templates.append(template)
                                self.default_template_names.append(
                                    template.name
                                )
            except Exception:
                pass

    def resolve(
        self,
        template_names: list[str],
        requested_template_names: list[str] | None = None,
        allow_inactive: bool = False,
    ) -> list[Type[TemplateABC]]:
        """Validates `template_names` (existence, plus `active`/
        `standalone` for `requested_template_names` — the subset the user
        actually typed, defaulting to all of `template_names`) and returns
        them, plus their transitive `dependencies`, in install order.

        Raises TemplateNotFoundError, TemplateInactiveError or
        TemplateNotStandaloneError for an invalid request.
        """
        if requested_template_names is None:
            requested_template_names = template_names

        nonexistent_templates = [
            name for name in template_names if name not in self.template_names
        ]
        if nonexistent_templates:
            raise TemplateNotFoundError(', '.join(nonexistent_templates))

        templates_by_name = {t.name: t for t in self.templates}

        if not allow_inactive:
            for name in requested_template_names:
                if not templates_by_name[name].active:
                    raise TemplateInactiveError(name)

        for name in requested_template_names:
            template = templates_by_name[name]
            if not template.standalone:
                dependents = sorted(
                    t.name for t in self.templates if name in t.dependencies
                )
                raise TemplateNotStandaloneError(name, dependents)

        exclusive_groups: dict[str, list[str]] = {}
        for name in requested_template_names:
            group = templates_by_name[name].exclusive_group
            if group is not None:
                exclusive_groups.setdefault(group, []).append(name)

        # Only reject requesting two members of the same exclusive group
        # *together*, in the same command (e.g. `init pipenv uv`).
        # Requesting just one when a *different* member is already
        # installed (e.g. `add_template uv` on a pipenv project) is a
        # deliberate swap, not a conflict — each such template's
        # post_install is responsible for replacing whatever the project
        # currently uses.
        for group, names in exclusive_groups.items():
            if len(names) > 1:
                raise TemplateConflictError(names, group)

        resolved: list[Type[TemplateABC]] = []

        def add_with_dependencies(template: Type[TemplateABC]) -> None:
            if template.name in {t.name for t in resolved}:
                return

            for dependency in template.dependencies:
                if dependency in {t.name for t in resolved}:
                    continue

                dep_template = templates_by_name.get(dependency)
                if dep_template:
                    add_with_dependencies(dep_template)

            resolved.append(template)

        for template in self.templates:
            if template.name not in template_names:
                continue

            add_with_dependencies(template)

        return resolved
