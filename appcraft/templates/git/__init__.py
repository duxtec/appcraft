import subprocess
import sys

from infrastructure.framework.appcraft.utils.printer import Printer

from ..template_abc import TemplateABC


class GitTemplate(TemplateABC):
    active = True
    description = "\
Git Template sets up a Git repository for version control. It includes \
pre-configured files like `.gitignore` and a default repository structure, \
ensuring that the project is ready to be tracked and managed with Git."

    @classmethod
    def post_install(cls) -> None:
        try:
            subprocess.check_call(["python", "run_tools", "git", "init"])
        except subprocess.CalledProcessError as e:
            Printer.error(str(e))
            sys.exit(1)
