import sys

from infrastructure.core.printer import CorePrinter


def wait_for_key() -> None:
    CorePrinter.print("")
    CorePrinter.warning("Press any key to exit...", end="\n\n")

    if sys.platform == "win32":
        try:
            import msvcrt

            msvcrt.getch()
        except Exception:
            pass
        return

    import termios
    import tty

    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSANOW, old_settings)

    except (termios.error, OSError, ValueError):
        pass
