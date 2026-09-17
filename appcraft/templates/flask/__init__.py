from ..template_abc import TemplateABC


class FlaskTemplate(TemplateABC):
    active = True
    standalone = False
    description = (
        "Flask Template is the foundational setup for building Flask "
        "applications, providing the core configuration and structure that "
        "both the Flask UI Template and the Flask API Template extend. "
        "It establishes the base application factory, routing conventions, "
        "and project layout, ensuring a consistent starting point regardless "
        "of whether the resulting application serves rendered web pages, "
        "a JSON API, or both. By centralizing this shared setup, the template "
        "reduces boilerplate and keeps specialized extensions like the UI "
        "and API templates focused on their own concerns."
    )
