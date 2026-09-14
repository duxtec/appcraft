import importlib
import inspect
import pkgutil
from os import getcwd, listdir, sep
from os.path import abspath, isdir, join, relpath
from types import ModuleType
from typing import Any


class ImportManager:
    def __init__(self, package_name: str = "."):
        self.package_name = package_name

        if self.package_name and not self.package_name.startswith("."):
            self.abs_package_path: str = abspath(getcwd())
            self.abs_package_path = self._get_package_path()
            self.package_path = self.abs_package_path
        else:
            self.abs_package_path = inspect.stack()[1].filename
            self.abs_package_path = self.convert_package_to_directory(
                self.package_name
            )
            self.package_path = relpath(self.abs_package_path, start=getcwd())
            self.package_name = f"{self.package_path.replace(sep, '.')}"
            if self.package_name.endswith(".py"):
                self.package_name = self.package_name[:-3]

        self.package_path = self.package_path.replace("__init__.py", "")
        self.abs_package_path = self.abs_package_path.replace(
            "__init__.py", ""
        )

    def _import_package(self):
        try:
            return importlib.import_module(self.package_name)
        except ImportError as e:
            raise ImportError(
                f"Failed to import package '{self.package_name}': {e}"
            )

    def _get_package_path(self) -> str:
        try:
            package = self._import_package()
            if hasattr(package, "__file__") and package.__file__:
                package_file = package.__file__
                return package_file.replace("__init__.py", "")

            package_path = list(package.__path__)[0]
            return package_path.replace("__init__.py", "")
        except Exception as e:
            raise FileNotFoundError(
                f"Package or directory '{self.package_name}' not found: {e}"
            )

    def convert_package_to_directory(self, package_name: str):
        prefix = ""
        count = 0
        for char in package_name:
            if char == ".":
                count += 1
            else:
                break

        prefix += "../" * (count // 2)

        if count % 2 != 0:
            prefix += "./"

        package_name = package_name[count:]

        package_name = package_name.replace(".", sep)

        dir_path = join(self.abs_package_path, prefix + package_name)
        return dir_path

    def get_module_attributes(
        self,
        module_name: str = ".",
        include_privates: bool = False,
        include_imported: bool = False,
        recursive: bool = False,
    ):
        if self.package_name == ".":
            module = importlib.import_module(module_name)
        else:
            if not module_name.startswith("."):
                module_name = f".{module_name}"
            module = importlib.import_module(
                module_name, package=self.package_name
            )

        return self._extract_module_attributes(
            module, module_name, include_privates, include_imported, recursive
        )

    def _extract_module_attributes(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
        recursive: bool = False,
    ):
        if hasattr(module, "__file__") and not hasattr(module, "__path__"):
            return self._extract_module_attributes_from_file(
                module,
                module_name,
                include_privates,
                include_imported,
                recursive,
            )

        if hasattr(module, "__path__"):
            path = module.__path__[0]
            if "__init__.py" in listdir(path):
                return self._extract_module_attributes_from_package(
                    module,
                    module_name,
                    include_privates,
                    include_imported,
                    recursive,
                )

        return self._extract_module_attributes_from_directory(
            module,
            module_name,
            include_privates,
            include_imported,
            recursive,
        )

    def _extract_module_attributes_from_file(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
        recursive: bool = False,
    ) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        for name in dir(module):
            if not include_privates and name.startswith("_"):
                continue

            attr = getattr(module, name)

            try:
                attr_module_name = getattr(
                    attr, "__module__", getattr(attr, "__name__", "")
                )
            except RuntimeError:
                # Skips context-bound proxies
                # (e.g. Flask's `request`, `session`, `g`)
                # that raise when accessed outside an
                # active request/app context
                continue

            if attr_module_name == module.__name__ or include_imported:
                attributes[name] = attr
        return attributes

    def _extract_module_attributes_from_package(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
        recursive: bool = False,
    ) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        for name in dir(module):
            if not include_privates and name.startswith("_"):
                continue

            attr = getattr(module, name)

            if inspect.ismodule(attr):
                continue

            try:
                attr_module_name = getattr(
                    attr, "__module__", getattr(attr, "__name__", "")
                )
            except RuntimeError:
                # Skips context-bound proxies
                # (e.g. Flask's `request`, `session`, `g`)
                # that raise when accessed outside an
                # active request/app context
                continue

            # Same strict rule: only what __init__.py actually defines or
            # re-exports directly from this exact module counts here.
            if attr_module_name == module.__name__ or include_imported:
                attributes[name] = attr

        # Recurse into the package's own directory so submodules not
        # re-exported by __init__.py (e.g. use_cases/user/get.py) are
        # still discovered, without relying on Python's auto-exposed
        # submodule attributes (which would leak that submodule's own
        # imports, i.e. "imports of imports").
        if recursive:
            directory_attributes = (
                self._extract_module_attributes_from_directory(
                    module,
                    module_name,
                    include_privates,
                    include_imported,
                    recursive,
                )
            )
            for key, value in directory_attributes.items():
                attributes.setdefault(key, value)

        return attributes

    def _extract_module_attributes_from_directory(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
        recursive: bool = False,
    ) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        path = module.__path__[0]
        base_name = module.__name__

        for entry_name in listdir(path):
            full_entry_path = join(path, entry_name)

            if entry_name.endswith('.py') and entry_name != '__init__.py':
                submodule_stem = entry_name[:-3]
                full_submodule_name = f"{base_name}.{submodule_stem}"

                submodule = importlib.import_module(full_submodule_name)
                submodule_attrs = self._extract_module_attributes_from_file(
                    submodule,
                    full_submodule_name,
                    include_privates,
                    include_imported,
                )
                attributes[submodule_stem] = submodule_attrs

            elif (
                recursive
                and isdir(full_entry_path)
                and entry_name != "__pycache__"
            ):
                full_subpackage_name = f"{base_name}.{entry_name}"

                subpackage = importlib.import_module(full_subpackage_name)
                subpackage_attrs = self._extract_module_attributes(
                    subpackage,
                    full_subpackage_name,
                    include_privates,
                    include_imported,
                )
                attributes[entry_name] = subpackage_attrs

        return attributes

    def _is_part_of_package(
        self,
        attr_module_name: str,
        module_name: str,
        include_imported: bool = False,
    ) -> bool:
        if attr_module_name.startswith(module_name):
            return True
        if attr_module_name.startswith(self.package_name):
            return True
        return include_imported

    def _format_module_name(self, attr_module_name: str, module_name: str):
        attr_module_name = attr_module_name.replace(self.package_name, "")
        return attr_module_name.replace(module_name, "").strip()

    def create_import_strings(
        self, list: bool = False, relative: bool = False
    ):
        import_list = self.create_import_list(relative=relative)

        return "\n".join(import_list)

    def create_import_list(self, relative: bool = False):
        self.package_path = self._get_package_path()
        module_names = [
            name for _, name, _ in pkgutil.iter_modules([self.package_path])
        ]

        if not module_names:
            module_names = [""]

        import_strings: list[str] = []

        # import_strings_def = self._build_import_string

        for name in module_names:
            if self._is_valid_module(name):
                import_string = self._build_import_string(name, relative)
                if import_string:
                    import_strings.append(import_string)
        return import_strings

    def _build_import_string(self, module_name: str, relative: bool = False):
        if module_name and not module_name.startswith("."):
            module_name = f".{module_name}"

        package_name = f"{self.package_name}{module_name}"

        attributes = self.get_module_attributes(module_name)

        if attributes:
            attr_names = ", ".join(attributes.keys())
            import_string = (
                f"from {module_name} import {attr_names}"
                if relative
                else f"from {package_name} import {attr_names}"
            )

            return import_string

    def _is_valid_module(self, module_name: str):
        return module_name not in {
            "__init__",
            self.package_name,
            "initializer",
        }

    def update_init_file(self):
        import_strings = self.create_import_strings(relative=True)
        init_file_path = join(self.package_path, "__init__.py")
        with open(init_file_path, "w") as f:
            f.write(import_strings)
        return import_strings
