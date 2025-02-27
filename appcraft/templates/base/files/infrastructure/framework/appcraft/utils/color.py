import colorsys
from typing import List, Union

from infrastructure.framework.appcraft.core.config import Config


class Color:
    @staticmethod
    def RGBtoHSL(rgb, array=False) -> Union[str, List[Union[int, float]]]:
        if len(rgb) == 7:
            red = int(rgb[1:3], 16)
            green = int(rgb[3:5], 16)
            blue = int(rgb[5:7], 16)
        else:
            red = int(rgb[1] * 2, 16)
            green = int(rgb[2] * 2, 16)
            blue = int(rgb[3] * 2, 16)

        red /= 255.0
        green /= 255.0
        blue /= 255.0

        hue, lightness, saturations = colorsys.rgb_to_hls(red, green, blue)

        hue = round(hue * 360)
        saturation = round(saturations * 100, 2)
        lightness = round(lightness * 100, 2)

        if array:
            return [hue, saturation, lightness]
        return f"hsl({hue},{saturation}%,{lightness}%)"

    @staticmethod
    def HSLtoRGB(hsl, array=False):
        hue, saturation, lightness = hsl
        hue /= 360.0
        saturation /= 100.0
        lightness /= 100.0

        red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)

        red = round(red * 255)
        green = round(green * 255)
        blue = round(blue * 255)

        if array:
            return [red, green, blue]

        red = f"{red:02x}"
        green = f"{green:02x}"
        blue = f"{blue:02x}"
        return f"#{red}{green}{blue}"

    @staticmethod
    def palette():
        try:
            theme = Config().get("theme")
            color1 = theme["color1"]
            color2 = theme["color2"]
        except Exception:
            theme = {"color1": "#FFFFFF", "color2": "#000000"}
            color1 = theme["color1"]
            color2 = theme["color2"]

        hsl1 = list(Color.RGBtoHSL(color1, True))
        hsl2 = list(Color.RGBtoHSL(color2, True))

        palette_dict = {
            "darkcolor": [[] for _ in range(3)],
            "lightcolor": [[] for _ in range(3)],
            "brightcolor": [[] for _ in range(3)],
        }

        palette_dict["darkcolor"][0].append("#000")
        palette_dict["lightcolor"][0].append("#FFF")

        for i in range(5, 30, 5):
            # Generate dark colors
            hsl1_dark = hsl1[:]
            hsl2_dark = hsl2[:]
            hsl1_dark[2] = i
            hsl2_dark[2] = i
            darkcolor1 = Color.HSLtoRGB(hsl1_dark)
            darkcolor2 = Color.HSLtoRGB(hsl2_dark)
            palette_dict["darkcolor"][1].append(darkcolor1)
            palette_dict["darkcolor"][2].append(darkcolor2)

            # Generate light colors
            hsl1_light = hsl1[:]
            hsl2_light = hsl2[:]
            hsl1_light[2] = 100 - i
            hsl2_light[2] = 100 - i
            lightcolor1 = Color.HSLtoRGB(hsl1_light)
            lightcolor2 = Color.HSLtoRGB(hsl2_light)
            palette_dict["lightcolor"][1].append(lightcolor1)
            palette_dict["lightcolor"][2].append(lightcolor2)

            # Generate bright colors
            hsl1_bright = hsl1[:]
            hsl2_bright = hsl2[:]
            hsl1_bright[2] = 50
            hsl2_bright[2] = 50
            old_s1 = hsl1_bright[1]
            old_s2 = hsl2_bright[1]
            hsl1_bright[1] = 115 - (i + 10 * (i // 5))
            hsl2_bright[1] = 115 - (i + 10 * (i // 5))
            brightcolor1 = Color.HSLtoRGB(hsl1_bright)
            brightcolor2 = Color.HSLtoRGB(hsl2_bright)
            hsl1_bright[1] = old_s1
            hsl2_bright[1] = old_s2
            palette_dict["brightcolor"][1].append(brightcolor1)
            palette_dict["brightcolor"][2].append(brightcolor2)

        return palette_dict
