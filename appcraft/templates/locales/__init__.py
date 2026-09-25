from ..template_abc import TemplateABC


class LocalesTemplate(TemplateABC):
    # Temporarily inactive: ships a Pipfile declaring real dependencies
    # (polib, ...) but no pyproject.toml equivalent — TemplateAdder only
    # copies a Pipfile for Pipenv-based projects, so for the default
    # (Poetry) a project this template's own imports fail until the
    # framework's runtime auto-install self-heals them, unreliably.
    # Re-activate once a pyproject.toml fragment is added.
    active = False
    description = "\
Locale Template provides a structured way to manage multiple languages in \
your application. It includes pre-configured localization files, making it \
easier to handle translations and internationalization."
