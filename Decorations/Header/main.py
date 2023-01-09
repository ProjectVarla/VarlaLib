from math import ceil, floor
from os import popen

from conf import settings

from ..Colors import Colorize, Colors

TOP_TEXT: str = (
    settings.APP_TYPE.upper() if "APP_TYPE" in settings.dict() else "PROJECT"
)
BOTTOM_TEXT: str = (
    settings.APP_NAME.upper() if "APP_NAME" in settings.dict() else "VARLA-NEWAPP"
)


# varla_logo_slices = [
#     Colorize(
#         "██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ ",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     Colorize(
#         "██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     Colorize(
#         "██║   ██║███████║██████╔╝██║     ███████║",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     Colorize(
#         "╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     Colorize(
#         " ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     Colorize(
#         "  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
#         foreground=FG.LIGHT_CYAN,
#     ),
#     # "\033[36m██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ \033[0m",
#     # "\033[36m██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗\033[0m",
#     # "\033[36m██║   ██║███████║██████╔╝██║     ███████║\033[0m",
#     # "\033[36m╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║\033[0m",
#     # "\033[36m ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║\033[0m",
#     # "\033[36m  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\033[0m"
# ]


varla_logo_slices = [
    "██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ ",
    "██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗",
    "██║   ██║███████║██████╔╝██║     ███████║",
    "╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║",
    " ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║",
    "  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
]


def header(top_text: str = "", bottom_text: str = ""):
    top_text = top_text if top_text else TOP_TEXT
    bottom_text = bottom_text if bottom_text else BOTTOM_TEXT

    print(varla_text(top_text, bottom_text))


def varla_text(top_text: str, bottom_text: str):
    rows, columns = popen("stty size", "r").read().split()
    columns = max(int(columns), 44)
    output = ""
    output += (
        f"╔═╡ { Colorize(top_text,foreground=Colors.FG.YELLOW,style=Colors.MD.BOLD) } ╞{'═'*floor(columns-(len(top_text)+8))}═╗\n"
        + f"║{' '*floor(columns-2)}║\n"
    )
    for i in varla_logo_slices:
        text = Colorize(i, foreground=Colors.FG.LIGHT_CYAN)
        output += f"║{' '*int(((columns-len(text))/2)+4)}{text}{' '*int((ceil((columns-len(text))/2.0))+5)}║\n"

    output += (
        f"║{' '*floor(columns-2)}║\n"
        + f"╚{'═'*floor(columns-(len(bottom_text)+7))}╡ { Colorize(bottom_text,foreground=Colors.FG.YELLOW,style=Colors.MD.BOLD)} ╞═╝"
    )
    return output
