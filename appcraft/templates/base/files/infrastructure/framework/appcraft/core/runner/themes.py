from typing import TYPE_CHECKING, Any

from infrastructure.framework.appcraft.utils.color import Color

if TYPE_CHECKING:
    from prompt_toolkit.styles import Style


class RunnerThemes:
    palette = Color.palette()
    darkcolor = palette["darkcolor"]
    lightcolor = palette["lightcolor"]
    brightcolor = palette["brightcolor"]

    dark_style = "dark"
    light_style = "light"

    def __init__(self, theme: str = dark_style) -> None:
        self.theme = theme

    def _colors(self) -> list[list[Any]]:
        return self.darkcolor if self.theme == self.dark_style else self.lightcolor

    def build_prompt_style(self) -> "Style":
        """Builds the prompt_toolkit Style for the interactive menu.

        Only imports prompt_toolkit here — the rest of the runner system
        (including apply_theme/remove_theme below) works without it, so a
        project that never hits the interactive menu never needs it
        installed.
        """
        from prompt_toolkit.styles import Style

        darkcolor = self.darkcolor
        lightcolor = self.lightcolor

        if self.theme == self.dark_style:
            fgcolor, bgcolor = lightcolor, darkcolor
        else:
            fgcolor, bgcolor = darkcolor, lightcolor

        return Style.from_dict(
            {
                # Background and text color for dialog
                "dialog": f"bg:{bgcolor[0][0]} {fgcolor[0][0]}",
                # Background and text color for the frame label
                "dialog frame.label": f"bg:{bgcolor[2][2]} {fgcolor[0][0]} bold",
                # Background and text color for the body
                "dialog.body": f"bg:{bgcolor[1][2]} {fgcolor[0][0]}",
                # Background color for the shadow
                "dialog shadow": f"{fgcolor[0][0]}",
                # Text color for selected radio item
                "radio-selected": f"fg:{bgcolor[2][2]} {bgcolor[2][2]}",
                # Text color for unselected radio item
                "radio": f"fg:{bgcolor[1][2]} {fgcolor[0][0]}",
            }
        )

    def apply_theme(self) -> None:
        bgcolor = self._colors()[1][2].lstrip("#")

        r = int(bgcolor[0:2], 16)
        g = int(bgcolor[2:4], 16)
        b = int(bgcolor[4:6], 16)

        hex_color = f"rgb:{r:02x}/{g:02x}/{b:02x}"
        try:
            print(f"\033]11;{hex_color}\007", end="")
        except Exception:
            pass

    def remove_theme(self) -> None:
        try:
            # OSC 111 resets the background to the terminal's own default,
            # instead of overwriting it with a fixed color.
            print("\033]111\007", end="")
        except Exception:
            pass
