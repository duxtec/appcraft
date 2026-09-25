#!/usr/bin/env python3
"""Generates the "Available Versions" page (versions/index.rst) by
scanning a docs root directory for version-named sibling folders,
instead of hand-maintaining the list inside every frozen version's
source tree.

Usage:
    python generate_versions_page.py <docs_root> <output_rst> [--include VERSION ...]

<docs_root> is a directory whose immediate subdirectories are version
folders (e.g. a checkout of the accumulating `docs` branch, where each
release's own folder lives at <docs_root>/<version>/). --include adds
one more version to the list even if it doesn't have a folder there
yet — used when freezing a new release before its folder has been
copied into <docs_root>.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from packaging.version import InvalidVersion, Version

_SKIP_NAMES = {"build", "agents", "scripts", "latest"}


def discover_versions(docs_root: Path) -> list[str]:
    found: list[str] = []
    for child in docs_root.iterdir():
        if (
            not child.is_dir()
            or child.name in _SKIP_NAMES
            or child.name.startswith(".")
        ):
            continue
        try:
            Version(child.name)
        except InvalidVersion:
            continue
        found.append(child.name)
    return found


def render(versions: list[str]) -> str:
    ordered = sorted(versions, key=Version, reverse=True)
    latest = ordered[0]

    lines = [
        ".. AppCraft Documentation master file",
        "",
        "",
        "Versions",
        "====================================",
        "",
        "This documentation contains multiple versions. Select the "
        "version you want to view:",
        "",
        "**Available Versions:**",
        "",
        "",
        f"- `latest (currently {latest}) <../../latest/index.html>`_",
    ]
    lines += [f"- `{v} <../../{v}/index.html>`_" for v in ordered]
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_root", type=Path)
    parser.add_argument("output_rst", type=Path)
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Version(s) to add even if not yet a folder in docs_root",
    )
    args = parser.parse_args()

    versions = set(discover_versions(args.docs_root)) | set(args.include)
    if not versions:
        print("No versions found — nothing to write.", file=sys.stderr)
        sys.exit(1)

    args.output_rst.parent.mkdir(parents=True, exist_ok=True)
    args.output_rst.write_text(render(list(versions)), encoding="utf-8")
    print(
        f"Wrote {len(versions)} version(s) to {args.output_rst}; "
        f"latest = {sorted(versions, key=Version, reverse=True)[0]}"
    )


if __name__ == "__main__":
    main()
