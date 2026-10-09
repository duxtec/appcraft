from infrastructure.git.toml_edit import has_table, set_value

_PYPROJECT_PATH = "pyproject.toml"


def write_pyproject_version(version: str) -> None:
    # PEP 621 ([project]) and Poetry ([tool.poetry]) keep the version in
    # different tables — update whichever one this project actually uses.
    with open(_PYPROJECT_PATH, "r") as file:
        text = file.read()

    for table in ("project", "tool.poetry"):
        if has_table(text, table):
            text = set_value(text, "version", version, table=table)

    with open(_PYPROJECT_PATH, "w") as file:
        file.write(text)
