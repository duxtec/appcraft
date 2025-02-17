import os
import toml
import subprocess
import shutil


class TemplateAdder:
    def __init__(self):
        pass

    def add_template(self, template_name):
        current_dir = os.getcwd()

        template_dir = os.path.join(
            os.path.dirname(__file__), '..', 'template', template_name,
        )

        template_files_dir = os.path.join(
            template_dir, "files"
        )

        if not os.path.exists(template_files_dir):
            raise FileNotFoundError(
                f"The template '{template_name}' does not exist. "
                "Run 'appcraft list-templates' to see the available templates."
            )

        for item in os.listdir(template_files_dir):
            s = os.path.join(template_files_dir, item)
            d = os.path.join(current_dir, item)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                self._copy_directory_contents(s, d)
            else:
                if os.path.exists(d) and not self.can_overwrite(d):
                    pass
                else:
                    shutil.copy2(s, d)

            project_template_folder = os.path.join(
                current_dir, "infrastructure", "framework",
                "appcraft", "templates", template_name
            )

            template_file = os.path.join(
                template_dir, "__init__.py"
            )
            if not os.path.exists(project_template_folder):
                os.makedirs(project_template_folder)

            shutil.copy2(template_file, project_template_folder)

    def merge_pipfiles(self, template_name):
        base_pipfile_path = "Pipfile"
        template_dir = os.path.join(
            os.path.dirname(__file__), '..', 'template', template_name
        )
        pipfile_template = os.path.join(template_dir, "files", "Pipfile")

        try:
            with open(base_pipfile_path, 'r') as base_file:
                base_pipfile = toml.load(base_file)

            with open(pipfile_template, 'r') as custom_file:
                custom_pipfile = toml.load(custom_file)

            for section in ['packages', 'dev-packages']:
                if section in custom_pipfile:
                    if section not in base_pipfile:
                        base_pipfile[section] = {}
                    for package, version in custom_pipfile[section].items():
                        base_pipfile[section][package] = version

            with open(base_pipfile_path, 'w') as base_file:
                toml.dump(base_pipfile, base_file)

        except FileNotFoundError:
            return
            # print(f"Error: {e}. Make sure the Pipfile path is correct.")
        except subprocess.CalledProcessError as e:
            print(f"\
Error during the addition of dependencies for template '{template_name}': {e}")

    def _copy_directory_contents(self, src_dir, dst_dir):
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                self._copy_directory_contents(s, d)
            else:
                if os.path.exists(d) and not self.can_overwrite(d):
                    pass
                else:
                    shutil.copy2(s, d)

    def can_overwrite(self, file_path):
        # Does not allow overwriting any file.
        # Checks if the file already exists
        # Returns True if the file does not exist
        return not os.path.exists(file_path)
