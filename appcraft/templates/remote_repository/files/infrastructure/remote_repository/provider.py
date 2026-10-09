import importlib

from application.ports.remote_repository import RemoteRepositoryPort
from infrastructure.core.config import Config

_default_remote_repository_adapter: RemoteRepositoryPort | None = None

# Other templates that ship their own RemoteRepositoryPort adapter (e.g.
# github, and later gitlab/bitbucket) are detected here at runtime via
# is_installed(), instead of being baked in at generation time — mirrors
# infrastructure/database/provider.py's _ADAPTER_BACKENDS.
_PLATFORM_BACKENDS: dict[str, tuple[str, str, str, str]] = {
    "github": (
        "infrastructure.framework.appcraft.templates.github",
        "GitHubTemplate",
        "infrastructure.remote_repository.github.adapter",
        "get_github_adapter",
    ),
}


def _load_backend_adapter(name: str) -> RemoteRepositoryPort | None:
    backend = _PLATFORM_BACKENDS.get(name)
    if backend is None:
        return None

    (
        template_module_name,
        template_class_name,
        adapter_module_name,
        adapter_getter_name,
    ) = backend

    try:
        template_module = importlib.import_module(template_module_name)
        template_class = getattr(template_module, template_class_name)

        if not template_class.is_installed():
            return None

        adapter_module = importlib.import_module(adapter_module_name)
        adapter_getter = getattr(adapter_module, adapter_getter_name)
        return adapter_getter()
    except Exception:
        return None


def _resolve_default_adapter() -> RemoteRepositoryPort | None:
    configured = Config().get("remote_repository").get("default_platform")
    if configured not in _PLATFORM_BACKENDS:
        configured = "github"

    fallback_order = [configured] + [
        name for name in _PLATFORM_BACKENDS if name != configured
    ]

    for name in fallback_order:
        adapter = _load_backend_adapter(name)
        if adapter is not None:
            return adapter

    return None


def get_default_remote_repository_adapter() -> RemoteRepositoryPort | None:
    """Returns the default adapter, shared across entrypoints — or None
    if no hosting-platform template (github, ...) is installed."""
    global _default_remote_repository_adapter
    if _default_remote_repository_adapter is None:
        _default_remote_repository_adapter = _resolve_default_adapter()
    return _default_remote_repository_adapter


def set_default_remote_repository_adapter(
    adapter: RemoteRepositoryPort,
) -> None:
    global _default_remote_repository_adapter
    _default_remote_repository_adapter = adapter
