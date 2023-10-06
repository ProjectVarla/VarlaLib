from __future__ import annotations
import asyncio

import readline
from os import system
import sys

from CommandCenter.v2.TyperTree import TyperTree
from VarlaLib.Context import context
from VarlaLib.Decorations import Colorize, Colors, header
from .test import test

typerTree: TyperTree


class VarlaCLI:
    @classmethod
    def parse_command(cls, message):

        typerTree: TyperTree = TyperTree()

        command: list[str] = message.split()

        if not command:
            return

        # registry_command = context.get_command(command)
        registry_command, idx = context.registry.find(command)
        if registry_command:
            registry_command.trigger(command[idx::])
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
            print(
                "\n"
                + Colorize(
                    text="  #   >>  ",
                    style=Colors.MD.BOLD,
                    foreground=Colors.FG.YELLOW,
                ),
                end="",
            )

    # @classmethod
    # def standby(cls):
    #     cls.clear()

    #     cls.say("Yes boss!")
    #     cls.say("How can I help you?")

    #     typerTree: TyperTree = TyperTree()

    #     while True:

    #         command: list[str] = cls.ask().split()

    #         if not command:
    #             continue

    #         registry_command = context.get_command(command)

    #         if registry_command:
    #             # print(registry_command)
    #             # pass
    #             registry_command.trigger(command)
    #         else:

    #             last_valid_cmd: int = -1
    #             nid: str = "varla"

    #             for idx, cmd in enumerate(command):
    #                 nid += f"_{cmd}"

    #                 if not typerTree.tree.contains(nid):
    #                     break

    #                 last_valid_cmd = idx

    #             if last_valid_cmd != -1 and typerTree.is_leaf(
    #                 command[: last_valid_cmd + 1]
    #             ):

    #                 if system(f"python3 bin/Varla {' '.join(command)}"):
    #                     system(
    #                         f"python3 bin/Varla {' '.join(command[: last_valid_cmd + 1])} --help"
    #                     )
    #             else:
    #                 system(
    #                     f"python3 bin/Varla {' '.join(command[: last_valid_cmd + 1])} --help"
    #                 )

    @classmethod
    def say(cls, *message: str, color=Colors.FG.CYAN, name="Varla"):

        # def print_during_input(string: str) -> None:
        sys.stdout.write(
            # Save cursor position
            "\N{ESC}7"
            # Add a new line
            "\N{LINE FEED}"
            # Move cursor up
            "\N{ESC}[A"
            # Insert blank line, scroll last line down
            "\N{ESC}[L"
            # Print string in the inserted blank line
            f'{Colorize(text=f"{name} >> ",style=Colors.MD.BOLD,foreground=color,)} {message[0]}\N{LINE FEED}'
            # Restore cursor position
            "\N{ESC}8"
            # Move cursor down
            "\N{ESC}[B"
        )
        sys.stdout.flush()

    @classmethod
    def ask(cls, message: str = ""):
        if message:
            cls.say(message)
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
            cls.say("Goodbye Boss!")
            raise KeyboardInterrupt

    @classmethod
    def error(cls, *message: str):
        cls.say(
            "Oops!, Something went wrong!",
            color=Colors.FG.RED,
        )
        cls.say(
            "This is what I managed to capture:",
            *message,
            color=Colors.FG.RED,
        )

    @classmethod
    def heartbeat(cls):
        cls.say("Connecting to main-frame...")
        cls.say("Connected!")

    @classmethod
    def history(cls):
        for i in range(readline.get_current_history_length()):
            print("         ", i, readline.get_history_item(i))

    @classmethod
    def clear(cls, top_text: str = "", bottom_text: str = "") -> None:
        system("cls||clear")
        header(top_text, bottom_text)

    # @classmethod
    @classmethod
    def standby(cls):
        cls.clear()

        cls.say("Yes boss!")
        cls.say("How can I help you?")

        cls.test("ws://localhost:8500/connect", cls)

    @classmethod
    def test(cls, uri, varla) -> None:

        try:
            import readline  # noqa
        except ImportError:  # Windows has no `readline` normally
            pass

        context.thread = None
        context.socket_id = None

        try:
            while True:
                message = varla.ask()

                if message == "status":
                    print(context)

                elif context.thread:
                    context.loop.call_soon_threadsafe(
                        context.inputs.put_nowait, message
                    )

                else:
                    cls.parse_command(message)
        except Exception as e:  # (KeyboardInterrupt, EOFError):  # ^C, ^D
            print("hello", e)
            raise e
