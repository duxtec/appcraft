from enum import Enum
from typing import List

from infrastructure.framework.appcraft.core.app_manager import AppManager


class COLORS(Enum):
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"
    BLACK = "30"
    DARK_GRAY = "90"
    LIGHT_RED = "91"
    LIGHT_GREEN = "92"
    LIGHT_YELLOW = "93"
    LIGHT_BLUE = "94"
    LIGHT_MAGENTA = "95"
    LIGHT_CYAN = "96"
    LIGHT_WHITE = "97"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_MAGENTA = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"
    BG_LIGHT_RED = "101"
    BG_LIGHT_GREEN = "102"
    BG_LIGHT_YELLOW = "103"
    BG_LIGHT_BLUE = "104"
    BG_LIGHT_MAGENTA = "105"
    BG_LIGHT_CYAN = "106"
    BG_LIGHT_WHITE = "107"

    BOLD = "1"
    DIM = "2"
    UNDERLINE = "4"
    REVERSED = "7"
    HIDDEN = "8"


class STYLES(Enum):
    BOLD = "1"
    DIM = "2"
    UNDERLINE = "4"
    REVERSED = "7"
    HIDDEN = "8"


class Printer:

    @classmethod
    def print(
        cls,
        message="",
        color: COLORS = COLORS.WHITE,
        styles: List[STYLES] = [],
        sep: str | None = " ",
        end: str | None = "\n",
        if_debug=False,
    ):
        if if_debug and not AppManager.debug_mode:
            return

        codes = []

        if isinstance(color, COLORS):
            codes.append(color.value)

        for style in styles:
            if isinstance(style, STYLES):
                codes.append(style.value)

        style_code = ";".join(codes)

        print(f"\033[{style_code}m{message}\033[0m", sep=sep, end=end)
        return message

    @classmethod
    def success(
        cls,
        message,
        sep: str | None = " ",
        end: str | None = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.GREEN,
            styles=[STYLES.BOLD],
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def error(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.RED,
            styles=[STYLES.BOLD],
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def warning(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message,
            color=COLORS.YELLOW,
            styles=[STYLES.BOLD],
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def info(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.BLUE,
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def title(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.MAGENTA,
            styles=[STYLES.BOLD, STYLES.UNDERLINE],
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def critical(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.RED,
            styles=[STYLES.BOLD, STYLES.REVERSED],
            sep=sep,
            end=end,
            if_debug=if_debug,
        )

    @classmethod
    def debug(
        cls,
        message,
        sep: str = " ",
        end: str = "\n",
        if_debug=False,
    ):
        return cls.print(
            message=message,
            color=COLORS.DARK_GRAY,
            sep=sep,
            end=end,
            if_debug=if_debug,
        )
