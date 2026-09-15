class TemplateNotFoundError(FileNotFoundError):
    def __init__(self, template_name: str, *args: object) -> None:
        if not args:
            args = (
                f"""\
The template '{template_name}' does not exist.
Run 'appcraft list_templates' to see the available templates.""",
            )

        super().__init__(*args)


class TemplateInactiveError(Exception):
    def __init__(self, template_name: str, *args: object) -> None:
        if not args:
            args = (
                f"""\
The template '{template_name}' is still under development (inactive) and \
is not installed by default.
Pass --install-inactive to install it anyway.""",
            )

        super().__init__(*args)


class TemplateConflictError(Exception):
    def __init__(
        self,
        template_names: list[str],
        exclusive_group: str,
        *args: object,
    ) -> None:
        if not args:
            args = (
                f"""\
Cannot install {', '.join(template_names)} together — they all belong to \
the '{exclusive_group}' exclusive group, only one of them can be \
installed at a time.""",
            )

        super().__init__(*args)


class TemplateNotStandaloneError(Exception):
    def __init__(
        self,
        template_name: str,
        dependents: list[str] | None = None,
        *args: object,
    ) -> None:
        if not args:
            if dependents:
                hint = (
                    f"Install one of these instead: {', '.join(dependents)}."
                )
            else:
                hint = "No other template depends on it yet."

            args = (
                f"""\
The template '{template_name}' cannot be installed standalone — it is only \
usable as a dependency of another template.
{hint}""",
            )

        super().__init__(*args)
