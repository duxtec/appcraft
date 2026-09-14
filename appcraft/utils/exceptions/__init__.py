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


class TemplateNotStandaloneError(Exception):
    def __init__(
        self,
        template_name: str,
        dependents: list[str] | None = None,
        *args: object,
    ) -> None:
        if not args:
            if dependents:
                hint = f"Install one of these instead: {', '.join(dependents)}."
            else:
                hint = "No other template depends on it yet."

            args = (
                f"""\
The template '{template_name}' cannot be installed standalone — it is only \
usable as a dependency of another template.
{hint}""",
            )

        super().__init__(*args)
