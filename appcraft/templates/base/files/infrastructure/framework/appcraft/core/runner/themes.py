from typing import Optional

from infrastructure.framework.appcraft.utils.color import Color
from prompt_toolkit.styles import Style


class RunnerThemes:
    palette = Color.palette()
    darkcolor = palette["darkcolor"]
    lightcolor = palette["lightcolor"]
    brightcolor = palette["brightcolor"]
    dark_style = Style.from_dict(
        {
            # Background and text color for dialog
            "dialog": f"bg:{darkcolor[0][0]} {lightcolor[0][0]}",
            # Background and text color for the frame label
            "dialog frame.label": f"\
bg:{darkcolor[2][2]} {lightcolor[0][0]} bold",
            # Background and text color for the body
            "dialog.body": f"bg:{darkcolor[1][2]} {lightcolor[0][0]}",
            # Background color for the shadow
            "dialog shadow": f"{lightcolor[0][0]}",
            # Text color for selected radio item
            "radio-selected": f"fg:{darkcolor[2][2]} {darkcolor[2][2]}",
            # Text color for unselected radio item
            "radio": f"fg:{darkcolor[1][2]} {lightcolor[0][0]}",
        }
    )

    light_style = Style.from_dict(
        {
            # Background and text color for dialog
            "dialog": f"bg:{lightcolor[0][0]} {darkcolor[0][0]}",
            # Background and text color for the frame label
            "dialog frame.label": f"\
bg:{lightcolor[2][2]} {darkcolor[0][0]} bold",
            # Background and text color for the body
            "dialog.body": f"bg:{lightcolor[1][2]} {darkcolor[0][0]}",
            # Background color for the shadow
            "dialog shadow": f"{lightcolor[0][0]}",
            # Text color for selected radio item
            "radio-selected": f"fg:{lightcolor[2][2]} {darkcolor[2][2]}",
            # Text color for unselected radio item
            "radio": f"fg:{lightcolor[1][2]} {darkcolor[0][0]}",
        }
    )
    style: Style = dark_style

    @classmethod
    def apply_theme(cls, style: Optional[Style] = None):
        style = style or cls.style
        if style is cls.dark_style:
            bgcolor = cls.darkcolor[1][2].lstrip("#")
        else:
            bgcolor = cls.lightcolor[1][2].lstrip("#")

        r = int(bgcolor[0:2], 16)
        g = int(bgcolor[2:4], 16)
        b = int(bgcolor[4:6], 16)

        hex_color = f"rgb:{r:02x}/{g:02x}/{b:02x}"
        try:
            print(f"\033]11;{hex_color}\007", end="")
        except Exception:
            pass

        print(f"\033]11;{hex_color}\007", end="")

    def remove_theme(self):
        try:
            print("\033]11;#000000\007", end="")
        except Exception:
            pass
