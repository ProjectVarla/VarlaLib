from __future__ import annotations

from os import popen
from typing import Any

from Models import Arrow, Pair
from pynput import keyboard

from ...Decorations import Colorize, Colors
from ..VarlaCLI import VarlaCLI as Varla


class Control:
    """"""

    output = ""
    ctrl: bool = False
    alt: bool = False
    shift: bool = False
    esc: bool = False

    count = 0

    # X,Y Rows,Columns
    cursor: Pair = Pair(0, 0)
    dimension: Pair

    on_enter_lambda: Any
    on_render_lambda: Any

    def __init__(self, on_enter, on_render, dimension) -> None:
        self.on_enter_lambda = on_enter
        self.on_render_lambda = on_render
        self.dimension = dimension

    def listen(self):
        """"""
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()

    def reset_modifiers(self):
        self.ctrl = False
        self.alt = False
        self.shift = False
        self.esc = False

    def go_up(self) -> bool:
        """"""

        if (self.cursor + Arrow.up).isWithin(self.dimension):
            self.cursor += Arrow.up
            return True

        return False

    def go_down(self) -> bool:
        """"""

        if (self.cursor + Arrow.down).isWithin(self.dimension):
            self.cursor += Arrow.down
            return True

        return False

    def go_left(self) -> bool:
        """"""

        if (self.cursor + Arrow.left).isWithin(self.dimension):
            self.cursor += Arrow.left
            return True

        return False

    def go_right(self) -> bool:
        """"""

        if (self.cursor + Arrow.right).isWithin(self.dimension):
            self.cursor += Arrow.right
            return True

        return False

    def on_enter(self):
        """"""
        self.stop()
        Varla.clear()
        print("exiting", self.count)
        #####

        # Lambda payload
        # if self.on_enter_lambda:
        self.on_enter_lambda(self.cursor)

        print("re-entring", self.count + 1)
        #####

        # self.print()
        self.listen()

    def on_back(self):
        # Lambda payload

        pass

    def on_press(self, key):
        """"""
        Varla.clear()
        print(key)
        ##### Modifiers ####

        if key == keyboard.Key.ctrl:
            self.ctrl = True
        elif key == keyboard.Key.shift:
            self.shift = True
        elif key == keyboard.Key.alt:
            self.alt = True
        elif key == keyboard.Key.esc:
            self.esc = True

        #### Arrows ####

        elif key == keyboard.Key.up:
            self.go_up()
            self.reset_modifiers()

        elif key == keyboard.Key.down:
            self.go_down()
            self.reset_modifiers()

        elif key == keyboard.Key.right:
            self.go_right()
            self.reset_modifiers()

        elif key == keyboard.Key.left:
            self.go_left()
            self.reset_modifiers()

        elif key == keyboard.Key.enter:
            self.on_enter()
            self.reset_modifiers()

        self.print()

    def on_release(self, key) -> bool:

        #### Exits ####

        if self.esc and self.ctrl:
            print("hello?")
            return False

        try:
            if self.ctrl and key.char == "c":
                return False
        except AttributeError:
            pass

        return True

    def stop(self):
        """"""
        self.esc = True
        self.ctrl = True

        self.on_release(keyboard.Key.esc)

        self.reset_modifiers()

    def options_bar(self):
        rows, columns = popen("stty size", "r").read().split()

        space = Colorize(
            " ",
            background=Colors.BG.LIGHT_GRAY,
            foreground=Colors.FG.BLACK,
            style=Colors.MD.BLINK,
        )

        self.output += "\n" + space

        self.output += Colorize(
            " | ", foreground=Colors.FG.BLACK, background=Colors.BG.LIGHT_GRAY
        ).join(
            [
                Colorize(
                    "CTRL",
                    background=Colors.BG.LIGHT_GRAY,
                    foreground=Colors.FG.BLACK,
                    style=Colors.MD.BLINK if self.ctrl else Colors.MD.NOTHING,
                ),
                Colorize(
                    "ALT",
                    background=Colors.BG.LIGHT_GRAY,
                    foreground=Colors.FG.BLACK,
                    style=Colors.MD.BLINK if self.alt else Colors.MD.NOTHING,
                ),
                Colorize(
                    "SHIFT",
                    background=Colors.BG.LIGHT_GRAY,
                    foreground=Colors.FG.BLACK,
                    style=Colors.MD.BLINK if self.shift else Colors.MD.NOTHING,
                ),
                Colorize(
                    "ESC",
                    background=Colors.BG.LIGHT_GRAY,
                    foreground=Colors.FG.BLACK,
                    style=Colors.MD.BLINK if self.esc else Colors.MD.NOTHING,
                ),
            ]
        )
        self.output += space * 20

        print(self.cursor)

    def print(self):

        self.output = self.on_render_lambda(self.cursor)
        self.options_bar()
        print(self.output)
