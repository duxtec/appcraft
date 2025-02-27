import os
import sys


def main():
    appcraft_root_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)))
    )

    base_template_path = os.path.join(
        appcraft_root_path, "templates", "base", "files"
    )

    sys.path.append(appcraft_root_path)
    sys.path.append(base_template_path)

    from appcraft.scripts.list_templates import list_templates
    from appcraft.scripts.project_init import project_init

    if len(sys.argv) < 2:
        print("Usage: appcraft <command> [options]")
        print("Available Commands: init, list_templates")
        sys.exit(1)

    commands = {"init": project_init, "list_templates": list_templates}

    command = sys.argv[1]

    sys.argv = sys.argv[1:]

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown Command: {command}")
        print(
            """\
Available Commands: init, list_templates"""
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
