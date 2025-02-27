from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.core.package_manager.interface import (
    PackageManagerInterface,
)

from .pip_manager import PipManager
from .pipenv_manager import PipenvManager
from .poetry_manager import PoetryManager


def PackageManager() -> PackageManagerInterface:
    default_pm = PoetryManager
    try:
        manager = AppManager().config["manager"] or "poetry"
        pms = {
            "poetry": PoetryManager,
            "pipenv": PipenvManager,
            "pip": PipManager,
        }
        return pms.get(manager, default_pm)()
    except Exception:
        return default_pm()
