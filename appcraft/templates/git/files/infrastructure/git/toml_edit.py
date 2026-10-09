import json
import re
from typing import Sequence, cast

_HEADER = re.compile(r"^\s*\[([^\[\]]+?)\]\s*(#.*)?$")


def has_table(text: str, table: str) -> bool:
    return _section(text, table) is not None


def set_value(text: str, key: str, value: object, table: str | None = None) -> str:
    """Replaces one key's value in place, keeping its indentation, its
    trailing comment and every other line of the file untouched. A missing
    key is appended to its section."""
    lines = text.splitlines(keepends=True)
    section = _section(text, table)
    if section is None:
        raise KeyError(f"table [{table}] not found")

    start, end = section
    pattern = re.compile(rf"^(\s*){re.escape(key)}\s*=\s*([^#]*?)(\s*#.*)?$")
    for index in range(start, end):
        body = lines[index].rstrip("\r\n")
        match = pattern.match(body)
        if match:
            newline = lines[index][len(body):]
            comment = match.group(3) or ""
            lines[index] = (
                f"{match.group(1)}{key} = {_literal(value)}{comment}{newline}"
            )
            return "".join(lines)

    insert_at = end
    while insert_at > start and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines.insert(insert_at, f"{key} = {_literal(value)}\n")
    return "".join(lines)


def _section(text: str, table: str | None) -> tuple[int, int] | None:
    lines = text.splitlines()
    headers = _headers(lines)

    if table is None:
        end = headers[0][0] if headers else len(lines)
        return 0, end

    for position, (index, name) in enumerate(headers):
        if name == table:
            following = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
            return index + 1, following
    return None


def _headers(lines: Sequence[str]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = _HEADER.match(line)
        if match:
            found.append((index, match.group(1).strip()))
    return found


def _literal(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple)):
        items = cast(Sequence[object], value)
        return "[" + ", ".join(_literal(item) for item in items) + "]"
    return json.dumps(str(value))
