import os
from typing import List
from .readkey import readKey
from .utilities import Utilities


class OptionSelector:
    header: str
    start_index: int
    options_size: int
    options: List[str]
    selected_option: int
    last_key_pressed_code: int

    def __init__(
        self,
        options: List[str],
        default_selected_option: int,
        header: str = "",
        options_size: int = 10,
    ):
        self.header = header
        self.start_index = 0
        self.options = options
        self.options_size = options_size
        self.selected_option = default_selected_option
        os.system("")  # enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607

    def getOption(self):
        print("\033[{0}m{1}  \033[m".format(40, self.header))

        for i in range(
            self.start_index,
            self.start_index + min(len(self.options), self.options_size),
        ):
            color_code = 7 if self.selected_option == i else 40
            print("\033[{0}m{1}  \033[m".format(color_code, self.options[i]))

        key = readKey(False)

        # Arrow Up Pressed
        if key in [b"\x00H", b"\xe0H"]:
            if self.selected_option > 0:
                self.selected_option -= 1
                if self.selected_option == self.start_index - 1:
                    self.start_index -= 1
        # Arrow Down Pressed
        elif key in [b"\xe0P", b"\x00P"]:
            if self.selected_option < len(self.options) - 1:
                if self.selected_option == self.start_index + self.options_size - 1:
                    self.start_index += 1
                self.selected_option += 1
        # Enter Pressed
        elif key == b"\r":
            return self.selected_option
        # Ctrl+C Pressed
        elif key == b"\x03":
            os._exit(1)

        Utilities.clearConsole()
        return self.getOption()