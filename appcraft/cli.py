import sys

from appcraft.scripts.list_templates import list_templates
from appcraft.scripts.project_init import project_init
from appcraft.scripts.save_template import save_template
from appcraft.utils import Printer


def main():
    if len(sys.argv) < 2:
        Printer.warning("Usage: appcraft <command> [options]")
        Printer.info("Available Commands: init, list_templates")
        sys.exit(1)

    commands = {
        "init": project_init,
        "list_templates": list_templates,
        "save_template": save_template,
    }

    command = sys.argv[1]

    sys.argv = sys.argv[1:]

    if command in commands:
        try:
            commands[command]()
        except Exception as e:
            Printer.error(f"Error: {e}")
            sys.exit(1)
    else:
        Printer.error(f"Unknown Command: {command}")
        Printer.info(
            """\
Available Commands: init, list_templates"""
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
