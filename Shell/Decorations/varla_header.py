from math import ceil, floor
from os import popen

from conf import settings

from ..Colors import Colorize
from ..Colors import Foreground as FG
from ..Colors import Modifier

TOP_TEXT = "PROJECT"
BOTTOM_TEXT = settings.APP_NAME

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


def varla_header():
    rows, columns = popen("stty size", "r").read().split()
    columns = max(int(columns), 44)

    print(
        f"╔═ { Colorize(TOP_TEXT,foreground=FG.YELLOW,style=Modifier.BOLD) } {'═'*floor(columns-(len(TOP_TEXT)+5))}╗"
    )
    print(f"║{' '*floor(columns-2)}║")
    for i in varla_logo_slices:
        print(
            f"║{' '*int(((columns-len(i))/2)+4)}{i}{' '*int((ceil((columns-len(i))/2.0))+5)}║"
        )
    print(f"║{' '*floor(columns-2)}║")
    print(
        f"╚{'═'*floor(columns-(len(BOTTOM_TEXT)+5))} { Colorize(BOTTOM_TEXT,foreground=FG.YELLOW,style=Modifier.BOLD)} ═╝"
    )
