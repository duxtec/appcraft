Prompt Toolkit Template
=============================

The **Prompt Toolkit Template** adds the ``prompt-toolkit`` dependency that powers the interactive menu shown by ``python run``/``python run_tools`` when a runner isn't fully specified on the command line.

Without it, the runner system still works — but only in "fully specified" mode: every ``python run``/``python run_tools`` call must name the exact file, class, and method, since there's no interactive picker to fall back on when more than one option exists. Installing this template is what makes the plain ``python run`` (with no arguments) prompt you to choose interactively.

There's nothing to configure — install it and the interactive menu is available from then on.
