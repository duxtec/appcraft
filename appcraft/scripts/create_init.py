import sys

from appcraft.utils import ImportManager


def create_init():
    root_dir = "./"
    sys.path.insert(0, root_dir)

    packages = ["core", "lib"]

    for package in packages:
        print(f"Processing the '{package}' folder:")
        manager = ImportManager(package)
        print(manager.package_path)
        import_text = '\n'.join(manager.update_init_file())
        print(import_text)
        print()
