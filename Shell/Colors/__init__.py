# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
# SGR color constants
# rene-d 2018

from enum import Enum

from tabulate import tabulate


class Foreground(Enum):
    DEFAULT = ""
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    BROWN = "33"
    BLUE = "34"
    PURPLE = "35"
    CYAN = "36"
    LIGHT_GRAY = "37"
    DARK_GRAY = "30"
    LIGHT_RED = "31"
    LIGHT_GREEN = "32"
    YELLOW = "33"
    LIGHT_BLUE = "34"
    LIGHT_PURPLE = "35"
    LIGHT_CYAN = "36"
    LIGHT_WHITE = "37"


class Modifier(Enum):
    NOTHING = "0"
    BOLD = "1"
    FAINT = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINK = "5"
    NEGATIVE = "7"
    CROSSED = "9"
    END = "0"


class Background(Enum):
    NOTHING = ""
    BLACK = "40"
    RED = "41"
    GREEN = "42"
    BROWN = "33"
    BLUE = "44"
    PURPLE = "45"
    CYAN = "46"
    LIGHT_GRAY = "47"
    DARK_GRAY = "40"
    LIGHT_RED = "41"
    LIGHT_GREEN = "42"
    YELLOW = "43"
    LIGHT_BLUE = "44"
    LIGHT_PURPLE = "45"
    LIGHT_CYAN = "46"
    LIGHT_WHITE = "47"


def Colorize(
    text: str = "",
    foreground: Foreground = Foreground.DEFAULT,
    background: Background = Background.NOTHING,
    style: Modifier = Modifier.NOTHING,
):

    foreground = foreground.value
    background = background.value
    style = style.value

    start_ansi = f"[{style}{';'if foreground else ''}{foreground}{';'if background else ''}{background}m"
    end_ansi = "\033[0m"

    if text == "":
        text = start_ansi

    return f"\033{start_ansi}{text}{end_ansi}"


def print_options():
    list = []
    for color in Foreground:
        list.append([Colorize(foreground=color, style=style) for style in Modifier])
        list[-1].append(Colorize(text=color.name, foreground=color))

    for color in Background:
        list.append([Colorize(background=color, style=style) for style in Modifier])
        list[-1].append(Colorize(text=color.name, background=color))

    header = [key.name for key in Modifier]
    header.append("Name")
    print(tabulate(list, headers=header))


if __name__ == "__main__":
    print_options()
