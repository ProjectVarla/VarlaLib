from __future__ import annotations

import readline
from os import system

from CommandCenter.TyperTree import TyperTree
from VarlaLib.Context import context
from VarlaLib.Decorations import Colorize, Colors, header


class VarlaCLI:
    @staticmethod
    def standby():

        VarlaCLI.clear()

        VarlaCLI.say("Yes boss!")
        VarlaCLI.say("How can I help you?")

        typerTree: TyperTree = TyperTree()

        while True:

            command: list[str] = VarlaCLI.ask().split()

            if not command:
                continue

            registry_command = context.get_command(command)

            if registry_command:
                registry_command.trigger()
            else:

                last_valid_cmd: int = -1
                nid: str = "varla"

                for idx, cmd in enumerate(command):
                    nid += f"_{cmd}"

                    if not typerTree.tree.contains(nid):
                        break

                    last_valid_cmd = idx

                if last_valid_cmd != -1 and typerTree.is_leaf(
                    command[: last_valid_cmd + 1]
                ):

                    if system(f"python3 bin/Varla {' '.join(command)}"):
                        system(
                            f"python3 bin/Varla {' '.join(command[: last_valid_cmd + 1])} --help"
                        )
                else:
                    system(
                        f"python3 bin/Varla {' '.join(command[: last_valid_cmd + 1])} --help"
                    )

    @staticmethod
    def say(*message: str, color=Colors.FG.CYAN, name="Varla"):
        print(
            Colorize(
                text=f"{name} >> ",
                style=Colors.MD.BOLD,
                foreground=color,
            ),
            *message,
        )

    @staticmethod
    def ask(message: str = ""):
        if message:
            VarlaCLI.say(message)
        try:
            return input(
                Colorize(
                    text="  #   >>  ",
                    style=Colors.MD.BOLD,
                    foreground=Colors.FG.YELLOW,
                )
            )
        except KeyboardInterrupt:
            print()
            VarlaCLI.say("Goodbye Boss!")
            exit()

    @staticmethod
    def error(*message: str):
        VarlaCLI.say(
            "Oops!, Something went wrong!",
            color=Colors.FG.RED,
        )
        VarlaCLI.say(
            "This is what I managed to capture:",
            *message,
            color=Colors.FG.RED,
        )

    @staticmethod
    def heartbeat():
        VarlaCLI.say("Connecting to main-frame...")
        VarlaCLI.say("Connected!")

    @staticmethod
    def history():
        for i in range(readline.get_current_history_length()):
            print("         ", i, readline.get_history_item(i))

    @staticmethod
    def clear(top_text: str = "", bottom_text: str = "") -> None:
        system("cls||clear")
        header(top_text, bottom_text)
