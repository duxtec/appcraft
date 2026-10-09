#!/usr/bin/env python3
"""Regenerates the /latest/ redirect stubs, pointing at whichever
version folder (immediate sibling directories of <docs_root>,
version-named) is numerically newest. GitHub Pages has no server-side
redirects, so these are tiny static HTML pages that redirect themselves.

One stub is generated per ``.html`` page that exists in the newest
version's own build output (``<docs_root>/build/<newest>/``), not just
the entry page — a deep link like ``latest/templates/index.html`` needs
its own stub mirroring that same path, or it 404s even though
``latest/index.html`` resolves fine.

Usage:
    python generate_latest_redirect.py <docs_root> [--include VERSION ...]

Writes <docs_root>/build/latest/<same relative path as in the newest
version's build output, for every .html page found there>.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from packaging.version import InvalidVersion, Version

_SKIP_NAMES = {"build", "agents", "scripts", "latest"}

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<title>Redirecting to Appcraft {version} docs</title>
<script>location.replace("{target}");</script>
</head>
<body>
<p>Redirecting to the latest version (<a href="{target}">\
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
    newest_build = args.docs_root / "build" / newest
    if not newest_build.is_dir():
        raise SystemExit(f"{newest_build} not found — build it first.")

    out_dir = args.docs_root / "build" / "latest"
    shutil.rmtree(out_dir, ignore_errors=True)

    pages = sorted(newest_build.rglob("*.html"))
    for page in pages:
        rel = page.relative_to(newest_build)
        ups = len(rel.parent.parts) + 1
        target = "../" * ups + newest + "/" + rel.as_posix()

        stub = out_dir / rel
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(
            _TEMPLATE.format(target=target, version=newest), encoding="utf-8"
        )

    print(f"latest -> {newest} ({len(pages)} page(s), {out_dir})")


if __name__ == "__main__":
    main()
