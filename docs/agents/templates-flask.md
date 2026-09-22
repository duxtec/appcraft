# Flask templates (`flask`, `flask_api`, `flask_ui`)

A variant of the [interchangeable-sibling-adapters pattern](architecture.md#the-interchangeable-sibling-adapters-via-is_installed-pattern) where the "siblings" are composable extensions rather than mutually-exclusive alternatives, plus a shared non-`standalone` base template — the precedent [templates-web-scraping.md](templates-web-scraping.md)'s family later copied for a case that also needed true interchangeable engines.

## `flask` (active, `standalone = False`)

The shared foundation — install `flask_api` and/or `flask_ui` instead; `flask` itself is rejected by `init`/`add_template` if requested directly (`TemplateNotStandaloneError`), since alone it has no routes to serve.

- `infrastructure/framework/flask/app.py` — `FlaskApp`, the application factory. Wires up Jinja context processors, then:
  - Initializes `FlaskSQLAlchemy` only if `SQLAlchemyTemplate.is_installed()` (warns and continues without a DB otherwise).
  - Calls `self.router.register_api_bp()` only if `FlaskAPITemplate.is_installed()`.
  - Calls `self.router.register_views_bp()` / `register_pages_bp()` only if `FlaskUITemplate.is_installed()`.
  - The 404 handler itself branches on `FlaskAPITemplate.is_installed()`/`FlaskUITemplate.is_installed()` to decide whether to return JSON or render `pages/404.html`.

  This is the pattern to follow for "does an optional sibling template change my behavior" logic — `is_installed()` checks, not template-generation-time branching, exactly as in [architecture.md](architecture.md#naming-and-layering-conventions).
- `infrastructure/framework/flask/router.py` — `FlaskRouter`: `register_api_bp()` (auto-discovers `Blueprint`s or `register()` functions under `presentation.web.api.v1.routes` via `ImportManager`, nests them under `/api/v1`), `register_views_bp()` (auto-discovers view functions under `presentation.web.ui.views`, one URL rule per function), `register_pages_bp()` (one static route per `.html` file under `presentation/web/ui/templates/pages/`).
- `infrastructure/framework/flask/sqlalchemy.py` — `FlaskSQLAlchemy`, the Flask-specific SQLAlchemy session/engine wiring (only imported/used when `sqlalchemy` is installed).
- `runners/main/flask.py` — the `Runner` subclass that starts `FlaskApp`.

## `flask_api` (active, `dependencies = ["flask"]`)

Adds `presentation/web/api/v1/routes/`, `presentation/web/api/v1/schemas/`, and `presentation/web/api/errors/` (error-handling scaffolding — some files here are deliberately left as empty placeholders for a project to fill in, not dead code to clean up). Routes/`register()` functions dropped under `presentation/web/api/v1/routes/` are picked up automatically by `FlaskRouter.register_api_bp()` above — no manual registration needed.

## `flask_ui` (active, `dependencies = ["flask"]`)

Adds `presentation/web/ui/{static,templates,views}/` — Jinja templates (`templates/{layouts,pages,partials,views}/`), static assets (`static/{css,js}/`), and view functions (`views/app.py`). Both `views/*.py` functions and `templates/pages/*.html` files are picked up automatically by `FlaskRouter` — no manual registration needed.

Installing `flask_api`, `flask_ui`, or both together are all valid — `flask`'s `app.py` adapts via the `is_installed()` checks above regardless of which combination is present.
