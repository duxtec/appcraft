# docs branch

This branch holds **only published documentation** — no application code.
It's the source GitHub Pages serves from, and it only ever grows: each
release (from any code branch — `v0-main`, `v0-beta`, a maintenance
branch, etc.) adds its own `<version>/` folder here; nothing is ever
removed or overwritten by a later release.

Layout:

- `<version>/source/` — the Sphinx source for that version, frozen at
  release time (e.g. `0.5.3/source/`, `0.6.0b0/source/`).
- `build/<version>/` — that version's built HTML output.
- `build/latest/` — a tiny static redirect to whichever `build/<version>/`
  is currently the newest (regenerated automatically by
  `docs/scripts/generate_latest_redirect.py`, from the main repo, every
  time a new version is added here).

This branch is updated automatically by `.github/workflows/docs.yml`
(on the main repo) whenever a GitHub Release is published — it is not
meant to be edited by hand.
