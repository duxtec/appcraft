"""Converts a generated project's dependency declarations between the
package-manager formats appcraft supports (Poetry's [tool.poetry.*] in
pyproject.toml, a PEP 621 pyproject.toml as used by uv, and a Pipfile as
used by Pipenv).

Used by the pipenv/uv templates' post_install, which each need to read
whatever format the project *currently* uses (it may have started as
Poetry, or already be a pipenv/uv project being swapped again) and
rewrite it as their own — so every function here is written in terms of a
package-manager-agnostic DependencySnapshot rather than assuming Poetry
is always the source.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Any, cast

import toml

_EXPLICIT_OPERATORS = (">=", "<=", "==", "!=", ">", "<", "~=")

_URL_FIELDS = (
    ("homepage", "Homepage"),
    ("repository", "Repository"),
    ("documentation", "Documentation"),
)


@dataclass
class DependencySnapshot:
    main: dict[str, str] = field(default_factory=lambda: {})
    groups: dict[str, dict[str, str]] = field(default_factory=lambda: {})
    python_version: str = "3.12"
    metadata: dict[str, Any] = field(default_factory=lambda: {})


# ---------------------------------------------------------------------
# Poetry-style constraint -> PEP 440
# ---------------------------------------------------------------------


def _split_version(version: str) -> list[int]:
    parts: list[int] = []
    for chunk in version.split("."):
        match = re.match(r"\d+", chunk)
        parts.append(int(match.group()) if match else 0)
    return parts


def _caret_upper_bound(version: str) -> str:
    parts = _split_version(version)
    while len(parts) < 3:
        parts.append(0)
    for i, value in enumerate(parts):
        if value != 0:
            bumped = parts[: i + 1]
            bumped[-1] += 1
            bumped += [0] * (3 - len(bumped))
            return ".".join(str(v) for v in bumped[:3])
    return "0.0.1"


def _tilde_upper_bound(version: str) -> str:
    dot_count = version.count(".")
    parts = _split_version(version)
    while len(parts) < 3:
        parts.append(0)
    if dot_count == 0:
        return f"{parts[0] + 1}.0.0"
    return ".".join(str(v) for v in [parts[0], parts[1] + 1, 0])


def poetry_constraint_to_pep440(constraint: Any) -> str:
    """Converts a single Poetry version constraint (e.g. "^2.13.4", "~1.2",
    "0.10.2", "*", ">=1.0,<2.0") to a PEP 440 specifier. Returns "" for
    "any version". Non-string constraints (Poetry also allows a table
    like {version = "...", extras = [...]}) fall back to "" rather than
    guessing.
    """
    if not isinstance(constraint, str):
        return ""

    constraint = constraint.strip()

    if not constraint or constraint == "*":
        return ""

    if any(constraint.startswith(op) for op in _EXPLICIT_OPERATORS):
        return constraint

    if constraint.startswith("^"):
        version = constraint[1:]
        return f">={version},<{_caret_upper_bound(version)}"

    if constraint.startswith("~"):
        version = constraint[1:]
        return f">={version},<{_tilde_upper_bound(version)}"

    # Bare version (e.g. "0.10.2") — Poetry treats this like a caret
    # requirement by default.
    return f">={constraint},<{_caret_upper_bound(constraint)}"


def bare_python_version(constraint: str) -> str:
    """Strips any operator prefix (^, ~, >=, ...) to get a bare X.Y[.Z]
    version, for contexts that want just a version number (e.g. Pipfile's
    [requires] python_version, which isn't a range).
    """
    match = re.search(r"\d+(\.\d+){0,2}", constraint)
    return match.group() if match else constraint


def _pep508_name_and_constraint(requirement: str) -> tuple[str, str]:
    match = re.match(
        r"\s*([A-Za-z0-9_.\-]+)\s*(\[[^\]]*\])?\s*(.*)", requirement
    )
    if not match:
        return requirement.strip(), ""
    return match.group(1), match.group(3).strip()


def _parse_author(entry: Any) -> dict[str, str]:
    if not isinstance(entry, str):
        return {"name": str(entry)}
    if "<" in entry and entry.endswith(">"):
        name, email = entry.rsplit("<", 1)
        return {"name": name.strip(), "email": email.rstrip(">").strip()}
    return {"name": entry.strip()}


def _load_toml(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return toml.load(file)


# ---------------------------------------------------------------------
# Reading the project's *current* dependency state, whatever format
# it's currently in
# ---------------------------------------------------------------------


def _read_from_poetry(pyproject: dict[str, Any]) -> DependencySnapshot:
    poetry = pyproject.get("tool", {}).get("poetry", {})
    raw_deps = poetry.get("dependencies", {})

    python_constraint = raw_deps.get("python", "3.12")

    main = {
        name: poetry_constraint_to_pep440(constraint)
        for name, constraint in raw_deps.items()
        if name.lower() != "python"
    }

    groups = {
        group_name: {
            name: poetry_constraint_to_pep440(constraint)
            for name, constraint in group.get("dependencies", {}).items()
        }
        for group_name, group in poetry.get("group", {}).items()
    }

    metadata = {
        key: poetry[key]
        for key in (
            "name",
            "version",
            "description",
            "license",
            "readme",
            "keywords",
            "classifiers",
            "homepage",
            "repository",
            "documentation",
        )
        if poetry.get(key)
    }
    if poetry.get("authors"):
        metadata["authors"] = [
            _parse_author(entry) for entry in poetry["authors"]
        ]

    return DependencySnapshot(
        main=main,
        groups=groups,
        python_version=bare_python_version(python_constraint),
        metadata=metadata,
    )


def _read_from_uv(pyproject: dict[str, Any]) -> DependencySnapshot:
    project = pyproject.get("project", {})

    main: dict[str, str] = {}
    for requirement in project.get("dependencies", []):
        name, constraint = _pep508_name_and_constraint(requirement)
        main[name] = constraint

    groups: dict[str, dict[str, str]] = {}
    for group_name, requirements in pyproject.get(
        "dependency-groups", {}
    ).items():
        group_deps: dict[str, str] = {}
        for requirement in requirements:
            name, constraint = _pep508_name_and_constraint(requirement)
            group_deps[name] = constraint
        groups[group_name] = group_deps

    python_version = bare_python_version(
        project.get("requires-python", "3.12")
    )

    metadata: dict[str, Any] = {}
    for key in ("name", "version", "description", "readme", "keywords",
                "classifiers"):
        if project.get(key):
            metadata[key] = project[key]
    if project.get("license"):
        license_value = project["license"]
        if isinstance(license_value, dict):
            license_table = cast(dict[str, Any], license_value)
            metadata["license"] = license_table.get("text")
        else:
            metadata["license"] = license_value
    if project.get("authors"):
        authors: list[dict[str, str]] = []
        for author in project["authors"]:
            if isinstance(author, dict):
                author_table = cast(dict[str, Any], author)
                authors.append(
                    {
                        "name": author_table.get("name", ""),
                        "email": author_table.get("email", ""),
                    }
                )
            else:
                authors.append(_parse_author(author))
        metadata["authors"] = authors
    urls = project.get("urls", {})
    for key, label in _URL_FIELDS:
        if urls.get(label):
            metadata[key] = urls[label]

    return DependencySnapshot(
        main=main,
        groups=groups,
        python_version=python_version,
        metadata=metadata,
    )


def _read_from_pipfile(pipfile: dict[str, Any]) -> DependencySnapshot:
    main = dict(pipfile.get("packages", {}))
    dev = dict(pipfile.get("dev-packages", {}))

    # Pipfile constraints are already pip-style (e.g. "*", ">=1.0,<2.0"),
    # just normalize the "any version" marker to "".
    main = {
        name: "" if constraint == "*" else constraint
        for name, constraint in main.items()
    }
    dev = {
        name: "" if constraint == "*" else constraint
        for name, constraint in dev.items()
    }

    python_version = pipfile.get("requires", {}).get(
        "python_version", "3.12"
    )

    return DependencySnapshot(
        main=main,
        groups={"dev": dev} if dev else {},
        python_version=python_version,
        # Pipfile carries no project metadata (name/authors/...).
        metadata={},
    )


def read_dependencies(target_dir: str) -> DependencySnapshot:
    """Reads whichever dependency format the project currently uses —
    Pipfile, a PEP 621 pyproject.toml (uv), or a Poetry-style
    pyproject.toml — and returns it as a package-manager-agnostic
    snapshot. If more than one happens to be present (e.g. re-running a
    conversion), Pipfile wins, then a PEP 621 pyproject.toml, then a
    Poetry one — matching which one a real project would actually be
    reading its dependencies from.
    """
    pipfile_path = os.path.join(target_dir, "Pipfile")
    pyproject_path = os.path.join(target_dir, "pyproject.toml")

    pyproject: dict[str, Any] = {}
    if os.path.exists(pyproject_path):
        try:
            pyproject = _load_toml(pyproject_path)
        except Exception:
            pyproject = {}

    if os.path.exists(pipfile_path):
        try:
            pipfile = _load_toml(pipfile_path)
            snapshot = _read_from_pipfile(pipfile)
            # Pipfile has no project metadata — pull it from pyproject.toml
            # if some was left behind (e.g. [tool.poetry] survives a
            # poetry -> pipenv conversion).
            if not snapshot.metadata and pyproject:
                if pyproject.get("project"):
                    snapshot.metadata = _read_from_uv(pyproject).metadata
                elif pyproject.get("tool", {}).get("poetry"):
                    snapshot.metadata = _read_from_poetry(pyproject).metadata
            return snapshot
        except Exception:
            pass

    if pyproject.get("project"):
        return _read_from_uv(pyproject)

    if pyproject.get("tool", {}).get("poetry"):
        return _read_from_poetry(pyproject)

    return DependencySnapshot()


def clear_dependency_sources(target_dir: str) -> None:
    """Removes every dependency-format artifact from the project, ahead
    of a template writing its own: Pipfile(.lock), and the dependency
    tables ([tool.poetry.dependencies]/[tool.poetry.group.*], or
    [project.dependencies]/[dependency-groups]) from pyproject.toml —
    while keeping pyproject.toml itself and any project metadata /
    [build-system] / other [tool.*] tables it holds.
    """
    for name in ("Pipfile", "Pipfile.lock"):
        path = os.path.join(target_dir, name)
        if os.path.exists(path):
            os.remove(path)

    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if not os.path.exists(pyproject_path):
        return

    pyproject = _load_toml(pyproject_path)
    changed = False

    poetry = pyproject.get("tool", {}).get("poetry")
    if poetry is not None:
        changed = (
            poetry.pop("dependencies", None) is not None or changed
        )
        changed = poetry.pop("group", None) is not None or changed

    if "project" in pyproject:
        changed = pyproject["project"].pop("dependencies", None) or changed
    if "dependency-groups" in pyproject:
        del pyproject["dependency-groups"]
        changed = True

    if changed:
        with open(pyproject_path, "w", encoding="utf-8") as file:
            toml.dump(pyproject, file)


# ---------------------------------------------------------------------
# Runtime package-manager selection (config/app.toml)
# ---------------------------------------------------------------------


def set_package_manager_config(target_dir: str, manager: str) -> None:
    """Updates (or appends) the `manager` key in the generated project's
    config/app.toml — the runtime counterpart of the scaffold-time package
    manager choice, read by PackageManagerBase() on every boot.
    """
    config_path = os.path.join(target_dir, "config", "app.toml")
    if not os.path.exists(config_path):
        return

    with open(config_path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    new_line = f'manager = "{manager}"'
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("manager"):
            lines[i] = new_line
            found = True
            break

    if not found:
        lines.append(new_line)

    with open(config_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
