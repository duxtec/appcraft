import os
import shutil
import stat

_HOOK_SOURCE = os.path.join(
    "infrastructure", "git", "hooks", "commit_msg.py"
)
_HOOKS_DIR = os.path.join(".git", "hooks")
_HOOK_TARGET = os.path.join(_HOOKS_DIR, "commit-msg")


def install_commit_msg_hook() -> None:
    if not os.path.isdir(_HOOKS_DIR):
        return

    shutil.copyfile(_HOOK_SOURCE, _HOOK_TARGET)

    mode = os.stat(_HOOK_TARGET).st_mode
    os.chmod(
        _HOOK_TARGET, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )
