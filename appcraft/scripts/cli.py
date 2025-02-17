import os
import sys


def main():
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..",
                "template", "base", "files"
            )
        )
    )

    from .project_init import project_init
    from .list_templates import list_templates

    if len(sys.argv) < 2:
        print("Usage: appcraft <command> [options]")
        print("Available Commands: init, list_templates")
        sys.exit(1)

    commands = {
        "init": project_init,
        "list_templates": list_templates
    }

    command = sys.argv[1]

    sys.argv = sys.argv[1:]

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown Command: {command}")
        print("""\
Available Commands: init, create_app, create_init, list_templates""")
        sys.exit(1)
