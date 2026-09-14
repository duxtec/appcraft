import re
from pathlib import Path

# Exact file/directory names or relative paths — matched literally
FILE_IGNORE_LIST: list[str] = [
    "infrastructure/framework/appcraft/templates",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "config",
]

# Regex patterns — matched against the file/dir name or full path
FILE_IGNORE_PATTERNS: list[str] = [
    r"__pycache__",
    r".ruff_cache",
    r".*\.pyc$",
    r".*\.pyo$",
    r"\.git$",
    r"\.venv$",
    r".*\.egg-info$",
    r"\.DS_Store$",
]

_compiled_ignore_patterns = [
    re.compile(pattern) for pattern in FILE_IGNORE_PATTERNS
]


def is_build_artifact(path: str | Path) -> bool:
    """Checks only the regex-based patterns (__pycache__, .pyc/.pyo, .git,
    .venv, *.egg-info, .DS_Store, .ruff_cache) — universal build/VCS
    artifacts that should never be copied anywhere, regardless of context.

    Unlike `is_ignored`, this ignores FILE_IGNORE_LIST, which encodes
    paths that are only meaningful for a specific caller (e.g. TemplateSaver
    not treating a target project's own template registry as tracked
    template source).
    """
    path_str = str(path).replace("\\", "/")
    name = Path(path_str).name

    for pattern in _compiled_ignore_patterns:
        if pattern.search(name) or pattern.search(path_str):
            return True

    return False


def is_ignored(path: str | Path) -> bool:
    """Checks whether a given file/directory path should be ignored,
    matching against both literal names/paths and regex patterns.
    """
    path_str = str(path).replace("\\", "/")
    name = Path(path_str).name

    # Exact match — either the full relative path or just the name
    if path_str in FILE_IGNORE_LIST or name in FILE_IGNORE_LIST:
        return True

    return is_build_artifact(path_str)
