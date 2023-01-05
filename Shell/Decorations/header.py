from math import ceil, floor
from os import popen

from conf import settings

from ..Colors import Colorize
from ..Colors import Foreground as FG
from ..Colors import Modifier

TOP_TEXT: str = (
    settings.APP_TYPE.upper() if "APP_TYPE" in settings.dict() else "PROJECT"
)
BOTTOM_TEXT: str = (
    settings.APP_NAME.upper() if "APP_NAME" in settings.dict() else "VARLA-NEWAPP"
)

varla_logo_slices = [
    Colorize(
        "██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ ",
        foreground=FG.LIGHT_CYAN,
    ),
    Colorize(
        "██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗",
        foreground=FG.LIGHT_CYAN,
    ),
    Colorize(
        "██║   ██║███████║██████╔╝██║     ███████║",
        foreground=FG.LIGHT_CYAN,
    ),
    Colorize(
        "╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║",
        foreground=FG.LIGHT_CYAN,
    ),
    Colorize(
        " ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║",
        foreground=FG.LIGHT_CYAN,
    ),
    Colorize(
        "  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
        foreground=FG.LIGHT_CYAN,
    ),
    # "\033[36m██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ \033[0m",
    # "\033[36m██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗\033[0m",
    # "\033[36m██║   ██║███████║██████╔╝██║     ███████║\033[0m",
    # "\033[36m╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║\033[0m",
    # "\033[36m ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║\033[0m",
    # "\033[36m  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\033[0m"
]


def header():
    print(varla_text())


def varla_text():
    rows, columns = popen("stty size", "r").read().split()
    columns = max(int(columns), 44)
    output = ""
    output += (
        f"╔═ { Colorize(TOP_TEXT,foreground=FG.YELLOW,style=Modifier.BOLD) } {'═'*floor(columns-(len(TOP_TEXT)+5))}╗\n"
        + f"║{' '*floor(columns-2)}║\n"
    )
    for i in varla_logo_slices:
        output += f"║{' '*int(((columns-len(i))/2)+4)}{i}{' '*int((ceil((columns-len(i))/2.0))+5)}║\n"

    output += (
        f"║{' '*floor(columns-2)}║\n"
        + f"╚{'═'*floor(columns-(len(BOTTOM_TEXT)+5))} { Colorize(BOTTOM_TEXT,foreground=FG.YELLOW,style=Modifier.BOLD)} ═╝"
    )
    return output
