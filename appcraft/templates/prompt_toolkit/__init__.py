from ..template_abc import TemplateABC


class PromptToolkitTemplate(TemplateABC):
    active = True
    description = "\
Prompt Toolkit Template adds the prompt-toolkit dependency, which powers \
the interactive runner menu (module/class/method selection) shown when a \
runner isn't fully specified via command-line arguments. The base \
template's runner system works without it as long as the full \
module/class/method path is always passed inline; install this template \
to get the interactive fallback menu too."
