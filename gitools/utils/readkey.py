import sys


class ReadKey:
    def __init__(self):
        try:
            self.impl = ReadKeyWindows()
        except ImportError:
            self.impl = ReadKeyUnix()

    def __call__(self):
        return self.impl()


class ReadKeyUnix:
    def __init__(self):
        import tty, termios

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class ReadKeyWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        result = b""
        while True:
            key = msvcrt.getch()
            result += key
            if not msvcrt.kbhit():
                break
        return result


def readKey(echo: bool = True):
    readKey = ReadKey()
    sys.stdout.flush()
    char = readKey()
    if echo:
        print(char, end="")
    return char