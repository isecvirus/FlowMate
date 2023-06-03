import time
from platform import system
from typing import Any
from util.colors import *
import sys

system = system().lower()

ARROW_UP = ""
ARROW_DOWN = ""
ARROW_RIGHT = ""
ARROW_LEFT = ""
NEXT = "next"
LAST = "last"

if (system == "windows"):
    import msvcrt  # MicroSoft Visual C RunTime

    ARROW_UP = b"H"
    ARROW_DOWN = b"P"
    ARROW_RIGHT = b"M"
    ARROW_LEFT = b"K"
elif (system == "linux"):
    import tty
    import termios

    ARROW_UP = b"A"
    ARROW_DOWN = b"B"
    ARROW_RIGHT = b"C"
    ARROW_LEFT = b"D"


class Prompt:
    def __init__(self, message: str, options: dict):
        self.message = message
        self.options = options
        self.default_option = None
        self.exit_char = b'q'
        self.submit_chars = [b"\r"]  # enter ' ' for space
        self.options_list = list(self.options.keys())
        try:
            self.selected = self.default_option if self.default_option and self.default_option in self.options else self.options_list[0]
        except IndexError:
            pass
        self.index = self.options_list.index(self.selected)
        self.selection_style = {"foreground": GREEN, "background": TRANSPARENT, "bold": BOLD, "underline": UNDERLINE,
                                "blink": WITHOUT, 'italic': WITHOUT, 'reverse': WITHOUT}
        self.wrap_selection_forward = False
        self.wrap_selection_backward = False
        self.box_selection = True if len(
            self.options_list) > 5 else False  # if options are more than 5 then make the options boxed
        self.forward_arrow = ARROW_RIGHT
        self.backward_arrow = ARROW_LEFT
        self.placeholder_foreground = GRAY + DIM
        self.placeholder_background = TRANSPARENT
        self.placeholder_pos = NEXT
        self.interval_update = 0.1

    def setIntervalUpdate(self, interval:int|float=0.1):
        self.interval_update = interval

    def getIntervalUpdate(self):
        return self.interval_update

    def setPlaceholderPosition(self, pos:str=NEXT):
        self.placeholder_pos = pos

    def getPlaceholderPosition(self) -> str:
        return self.placeholder_pos

    def setPlaceholderForeground(self, color:str):
        self.placeholder_foreground = color

    def getPlaceholderForeground(self) -> str:
        return self.placeholder_foreground

    def setPlaceholderBackground(self, color:str):
        self.placeholder_background = color

    def getPlaceholderBackground(self) -> str:
        return self.placeholder_background

    def setSelectionForeground(self, color: str):
        self.selection_style['foreground'] = color

    def getSelectionForeground(self) -> str:
        return self.selection_style['foreground']

    def isSelectionForeground(self, color: str) -> bool:
        return color == self.selection_style['foreground']

    def setSelectionBackground(self, color: str) -> None:
        self.selection_style['background'] = color

    def getSelectionBackground(self) -> str:
        return self.selection_style['background']

    def isSelectionBackground(self, color: str) -> bool:
        return color == self.selection_style['background']

    def setSelectionBold(self, value: bool = True) -> None:
        self.selection_style['bold'] = BOLD if value else WITHOUT

    def getSelectionBold(self) -> bool:
        return True if self.selection_style['bold'] else False

    def setSelectionUnderline(self, value: bool = True) -> None:
        self.selection_style['underline'] = UNDERLINE if value else WITHOUT

    def getSelectionUnderline(self) -> bool:
        return True if self.selection_style['underline'] else False

    def setSelectionBlink(self, value: bool = True) -> None:
        self.selection_style['blink'] = BLINK if value else WITHOUT

    def getSelectionBlink(self) -> bool:
        return True if self.selection_style['blink'] else False

    def setSelectionItalic(self, value: bool = True) -> None:
        self.selection_style['italic'] = ITALIC if value else WITHOUT

    def getSelectionItalic(self) -> bool:
        return True if self.selection_style['italic'] else False

    def setSelectionReverse(self, value: bool = True) -> None:
        self.selection_style['reverse'] = REVERSE if value else WITHOUT

    def getSelectionReverse(self) -> bool:
        return True if self.selection_style['reverse'] else False

    def setMessage(self, message: str) -> None:
        self.message = message

    def getMessage(self) -> str:
        return self.message

    def setDefaultOption(self, option: str) -> None:
        self.default_option = option

    def getDefaultOption(self) -> str:
        return self.default_option

    def setOptions(self, opts: dict) -> None:
        self.options = opts

    def getOptions(self) -> dict:
        return self.options

    def addOption(self, option: str, foreground: str = GRAY, background: str = TRANSPARENT, value: Any = '') -> None:
        self.options[option] = {"foreground": foreground, "background": background, "value": value}
        self.options_list = list(self.options.keys())

    def formatOption(self, foreground: str = GRAY, background: str = TRANSPARENT, value: Any = '') -> dict:
        return {"foreground": foreground, "background": background, "value": value}

    def removeOption(self, option: str) -> None:
        self.options.pop(option)

    def getOptionSettings(self, option: str) -> dict[str, bool]:
        if option in self.options:
            return self.options.get(option)

    def addSubmitChar(self, char: bytes) -> None:
        self.submit_chars.append(char)

    def isSubmitChar(self, char: str) -> bool:
        return char in self.submit_chars

    def removeSubmitChar(self, char: bytes) -> None:
        if char in self.submit_chars:
            self.submit_chars.remove(char)

    def getSubmitChars(self) -> list[bytes]:
        return self.submit_chars

    def setWrapSelection(self, forward: bool = True, backward: bool = True) -> None:
        self.wrap_selection_forward = forward
        self.wrap_selection_backward = backward

    def getWrapSelection(self) -> list[bool, bool, ...]:
        return [self.wrap_selection_forward, self.wrap_selection_backward]

    def setSelectionBoxed(self, value: bool = True):
        self.box_selection = value

    def setForwardArrow(self, arrow: bytes = ARROW_RIGHT):
        self.forward_arrow = arrow

    def getForwardArrow(self) -> str:
        return self.forward_arrow

    def setBackwardArrow(self, arrow: bytes = ARROW_LEFT):
        self.backward_arrow = arrow

    def getBackwardArrow(self) -> str:
        return self.backward_arrow

    def get_selected(self) -> str:
        return self.selected

    @staticmethod
    def format_option(value: str | int | float, foreground: str = GREEN, background: str = TRANSPARENT, placeholder:str="") -> dict:
        return {"foreground": foreground, "background": background, "value": value, "placeholder": placeholder}

    """
    +-----------------+-----------------+
    | Linux           | Windows         |
    +-----------------+-----------------+
    | \x1b[A          | \xe0H           | [UP]
    | \x1b[B          | \xe0P           | [BOTTOM]
    | \x1b[C          | \xe0M           | [RIGHT]
    | \x1b[D          | \xe0K           | [LEFT]
    | \r              | \r              | [ENTER]
    +-----------------+-----------------+
    | char1 = \x1b    | char1 = \xe0    |
    | char2 = [       | char2 = H/M/P/K |
    | char3 = A/B/C/D |                 |
    +-----------------------------------+
    """

    def run(self) -> Any:
        if len(self.options) >= 2:

            def format_options() -> str:
                style = ''.join(self.selection_style.values())

                placeholder = f" {self.placeholder_foreground + self.placeholder_background}{self.options[self.selected]['placeholder']}{RESET}"

                if self.box_selection :
                    return f"{style}{self.options[self.selected]['value']}{RESET}{placeholder}"
                else:
                    if self.placeholder_pos == NEXT:
                        return ' '.join([f"{style}{option}{RESET}{placeholder}" if option == self.selected else option for option in self.options])
                    elif self.placeholder_pos == LAST:
                        return ' '.join([f"{style}{option}{RESET}" if option == self.selected else option for option in self.options]) + placeholder

            if (system == "windows"):
                sys.stdout.write('\033[?25l')  # hide the cursor
                sys.stdout.flush()

                try:
                    while True:
                        # sys.stdout.write("\033[K")
                        print(f"\r\033[K{self.message} {format_options()}", end='')
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b'\xe0':
                                key = msvcrt.getch()

                                if key == self.forward_arrow:  # Right
                                    if self.wrap_selection_forward:
                                        self.index = (self.index + 1) % len(self.options_list)
                                    else:
                                        self.index = min(self.index + 1, len(self.options_list) - 1)
                                    self.selected = self.options_list[self.index]
                                elif key == self.backward_arrow:  # Left
                                    if self.wrap_selection_backward:
                                        self.index = (self.index - 1) % len(self.options_list)
                                    else:
                                        self.index = max(self.index - 1, 0)
                                    self.selected = self.options_list[self.index]

                            if key in self.submit_chars:
                                return self.options[self.selected]['value']
                        time.sleep(self.interval_update)
                except Exception:
                    pass

                sys.stdout.write('\033[?25h')  # show the cursor
                sys.stdout.flush()

            elif (system == "linux"):
                sys.stdout.write('\033[?25l')  # hide the cursor
                sys.stdout.flush()

                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(fd=sys.stdin)

                try:
                    while True:
                        print(f"\r\033[K{self.message} {format_options()}", end='')
                        ch = sys.stdin.read(1)  # get character
                        if ch == self.exit_char:
                            break
                        elif ch == "\x1b":  # control character
                            ch2 = sys.stdin.read(1)  # get next character
                            if ch2 == "[":  # A=up, B=down
                                ch3 = sys.stdin.read(1)  # get next character
                                if ch3 == self.forward_arrow:  # right
                                    if self.wrap_selection_forward:
                                        self.index = (self.index + 1) % len(self.options_list)
                                    else:
                                        self.index = min(self.index + 1, len(self.options_list) - 1)
                                    self.selected = self.options_list[self.index]
                                elif ch3 == self.backward_arrow:  # left
                                    if self.wrap_selection_backward:
                                        self.index = (self.index - 1) % len(self.options_list)
                                    else:
                                        self.index = max(self.index - 1, 0)
                                    self.selected = self.options_list[self.index]
                        elif ch in self.submit_chars:
                            return self.options[self.selected]['value']
                        time.sleep(self.interval_update)
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

                sys.stdout.write('\033[?25h')  # show the cursor
                sys.stdout.flush()
            else:
                exit("Not tested yet on '%s'" % system)


"""
Example:

prompt = Prompt
opts = {
    "ftp": prompt.format_option("ftp", placeholder="File transfer protocol"),
    "ssh": prompt.format_option("ssh"),
    "telnet": prompt.format_option("telnet", placeholder="A protocol used to share and receive data")
}

p1 = prompt(message="Add", options=opts)

p1.setForwardArrow(ARROW_RIGHT)
p1.setBackwardArrow(ARROW_LEFT)
p1.setSelectionBoxed(False)
p1.setPlaceholderForeground(GRAY+DIM)
p1.setPlaceholderPosition(LAST)

p1v = p1.run()
print(p1v)

"""
