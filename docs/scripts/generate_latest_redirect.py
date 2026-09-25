#!/usr/bin/env python3
"""Regenerates the /latest/ redirect stub, pointing at whichever
version folder (immediate sibling directories of <docs_root>,
version-named) is numerically newest. GitHub Pages has no server-side
redirects, so this is a tiny static HTML page that redirects itself.

Usage:
    python generate_latest_redirect.py <docs_root> [--include VERSION ...]

Writes <docs_root>/build/latest/index.html.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from packaging.version import InvalidVersion, Version

_SKIP_NAMES = {"build", "agents", "scripts", "latest"}

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=../{version}/index.html">
<link rel="canonical" href="../{version}/index.html">
<title>Redirecting to Appcraft {version} docs</title>
<script>location.replace("../{version}/index.html");</script>
</head>
<body>
<p>Redirecting to the latest version (<a href="../{version}/index.html">\
{version}</a>)&#8230;</p>
</body>
</html>
"""


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_root", type=Path)
    parser.add_argument("--include", action="append", default=[])
    args = parser.parse_args()

    versions = set(discover_versions(args.docs_root)) | set(args.include)
    if not versions:
        raise SystemExit("No versions found — nothing to redirect to.")

    newest = sorted(versions, key=Version, reverse=True)[0]

    out_dir = args.docs_root / "build" / "latest"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(
        _TEMPLATE.format(version=newest), encoding="utf-8"
    )
    print(f"latest -> {newest} ({out_dir / 'index.html'})")


if __name__ == "__main__":
    main()
