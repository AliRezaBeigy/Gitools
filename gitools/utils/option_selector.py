import os
from typing import List
from .readkey import readKey
from .utilities import Utilities


class OptionSelector:
    header: str
    options: List[str]
    selected_option: int
    last_key_pressed_code: int

    def __init__(self):
        os.system("")  # enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607

    def __init__(
        self, options: List[str], default_selected_option: int, header: str = ""
    ):
        self.header = header
        self.options = options
        self.selected_option = default_selected_option

    def getOption(self):
        print("\033[{0}m{1}  \033[m".format(40, self.header))

        for i in range(len(self.options)):
            color_code = 7 if self.selected_option == i else 40
            print("\033[{0}m{1}  \033[m".format(color_code, self.options[i]))

        key = readKey(False)

        # Arrow Up Pressed
        if key == b"\x00H":
            if self.selected_option > 0:
                self.selected_option -= 1
        # Arrow Down Pressed
        elif key == b"\x00P":
            if self.selected_option < len(self.options) - 1:
                self.selected_option += 1
        # Enter Pressed
        elif key == b"\r":
            return self.selected_option
        # Ctrl+C Pressed
        elif key == b"\x03":
            os._exit(1)

        Utilities.clearConsole()
        return self.getOption()