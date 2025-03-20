class TemplateNotFoundError(FileNotFoundError):
    def __init__(self, template_name: str, *args: object) -> None:
        if not args:
            args = (
                f"""\
The template '{template_name}' does not exist.
Run 'appcraft list-templates' to see the available templates.""",
            )

        super().__init__(*args)
