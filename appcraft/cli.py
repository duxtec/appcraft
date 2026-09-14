import sys

from .scripts.add_template import add_template
from .scripts.list_templates import list_templates
from .scripts.project_init import project_init
from .scripts.save_template import save_template
from .utils import Printer

COMMANDS = {
    "init": project_init,
    "list_templates": list_templates,
    "add_template": add_template,
    "save_template": save_template,
}


def main():
    if len(sys.argv) < 2:
        Printer.warning("Usage: appcraft <command> [options]")
        Printer.info(f"Available Commands: {', '.join(COMMANDS)}")
        sys.exit(1)

    command = sys.argv[1]

    sys.argv = sys.argv[1:]

    if command in COMMANDS:
        try:
            COMMANDS[command]()
        except Exception as e:
            Printer.error(f"Error: {e}")
            sys.exit(1)
    else:
        Printer.error(f"Unknown Command: {command}")
        Printer.info(f"Available Commands: {', '.join(COMMANDS)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
