from .package_manager_abc\
    import PackageManagerABC

from .pipenv_manager import PipenvManager
from .pip_manager import PipManager


def PackageManager(use_pipenv=True) -> PackageManagerABC:
    if use_pipenv:
        return PipenvManager()
    else:
        return PipManager()
