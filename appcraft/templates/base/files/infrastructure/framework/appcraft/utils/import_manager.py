import importlib
import inspect
import pkgutil
from os import getcwd, listdir, sep
from os.path import abspath, join, relpath
from types import ModuleType
from typing import Any, Dict, List


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

        self.package_path = f"{self.package_path.replace(f"__init__.py", '')}"
        self.abs_package_path = (
            f"{self.abs_package_path.replace(f"__init__.py", '')}"
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
            module, module_name, include_privates, include_imported
        )

    def _extract_module_attributes(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
    ):
        if hasattr(module, "__file__") and not hasattr(module, "__path__"):
            return self._extract_module_attributes_from_file(
                module, module_name, include_privates, include_imported
            )

        if hasattr(module, "__path__"):
            path = module.__path__[0]
            if "__init__.py" in listdir(path):
                return self._extract_module_attributes_from_package(
                    module, module_name, include_privates, include_imported
                )

        return self._extract_module_attributes_from_directory(
            module, module_name, include_privates, include_imported
        )

    def _extract_module_attributes_from_file(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
    ) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        for name in dir(module):
            if not include_privates and name.startswith("_"):
                continue

            attr = getattr(module, name)
            attr_module_name = getattr(
                attr, "__module__", getattr(attr, "__name__", "")
            )

            if self._is_part_of_package(
                attr_module_name, module.__name__, include_imported
            ):
                attributes[name] = attr
        return attributes

    def _extract_module_attributes_from_package(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
    ) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        for name in dir(module):
            if not include_privates and name.startswith("_"):
                continue

            attr = getattr(module, name)
            attr_module_name = getattr(
                attr, "__module__", getattr(attr, "__name__", "")
            )

            if self._is_part_of_package(
                attr_module_name, module_name, include_imported
            ):
                # key = self._format_module_name(attr_module_name, module_name)

                attributes[name] = attr
        return attributes

    def _extract_module_attributes_from_directory(
        self,
        module: ModuleType,
        module_name: str,
        include_privates: bool,
        include_imported: bool,
    ) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        path = module.__path__[0]

        module_dir = relpath(path, start=self.abs_package_path)

        module_path = f"{module_dir.replace(f".{sep}", '.')}"
        module_path = f"{module_path.replace(sep, '.')}"

        for file_name in listdir(path):
            if file_name.endswith('.py') and file_name != '__init__.py':
                submodule_name = f"{file_name[:-3]}"
                if not module_name.startswith("."):
                    submodule_name = f"{module_path}.{submodule_name}"

                submodule = self.get_module_attributes(f"{submodule_name}")

                attributes[f"{file_name[:-3]}"] = submodule

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

        import_strings: List[str] = []

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
