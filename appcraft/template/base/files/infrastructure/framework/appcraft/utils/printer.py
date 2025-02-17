from infrastructure.framework.appcraft.core.app_manager import AppManager


class COLORS:
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"


class Printer:
    _STYLES = {"bold": "1", "underline": "4", "reverse": "7"}

    @classmethod
    def print(
        cls,
        message="",
        color=COLORS.WHITE,
        bold=False,
        underline=False,
        reverse=False,
        sep: str | None = " ",
        end: str | None = "\n",
        if_debug=False
    ):
        if if_debug and not AppManager.debug_mode:
            return

        codes = []

        color = str(color)
        if isinstance(color, str):
            if color in COLORS.__dict__.values():
                codes.append(color)
            elif color and hasattr(COLORS, color.upper()):
                color_code = getattr(COLORS, color.upper())
                codes.append(color_code)

        if bold:
            codes.append(cls._STYLES["bold"])
        if underline:
            codes.append(cls._STYLES["underline"])
        if reverse:
            codes.append(cls._STYLES["reverse"])

        style_code = ";".join(codes)

        print(f"\033[{style_code}m{message}\033[0m", sep=sep, end=end)
        return message

    @classmethod
    def success(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.GREEN, bold=True,
            sep=sep, end=end, if_debug=if_debug
        )

    @classmethod
    def error(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.RED, bold=True,
            sep=sep, end=end, if_debug=if_debug
        )

    @classmethod
    def warning(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.YELLOW, bold=True,
            sep=sep, end=end, if_debug=if_debug
        )

    @classmethod
    def info(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.BLUE,
            sep=sep, end=end, if_debug=if_debug
        )

    @classmethod
    def title(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.MAGENTA, bold=True, underline=True,
            sep=sep, end=end, if_debug=if_debug
        )

    @classmethod
    def critical_alert(
        cls, message="", sep: str | None = " ",
        end: str | None = "\n", if_debug=False
    ):
        return cls.print(
            message, color=COLORS.RED, bold=True, reverse=True,
            sep=sep, end=end, if_debug=if_debug
        )
