from infrastructure.framework.appcraft.app.manager import AppManager
from infrastructure.framework.appcraft.core.package.manager import (
    PackageManager,
)

from ..pip import PipManager
from ..pipenv import PipenvManager
from ..poetry import PoetryManager
from ..uv import UvManager


def PackageManagerBase() -> PackageManager:
    default_pm = PoetryManager
    try:
        manager = AppManager().config.get("manager") or "poetry"
        pms = {
            "poetry": PoetryManager,
            "pipenv": PipenvManager,
            "pip": PipManager,
            "uv": UvManager,
        }
        return pms.get(manager, default_pm)()
    except Exception:
        return default_pm()
