import sys


class GetChar:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = GetCharWindows()
        except ImportError:
            self.impl = GetCharUnix()

    def __call__(self):
        return self.impl()


class GetCharUnix:
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


class GetCharWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def readChar():
    getChar = GetChar()
    sys.stdout.flush()
    char = getChar().decode('utf-8').replace('\r', '\r\n')
    print(char.replace('\x08', '\b \b').replace('\x03', ''), end='')
    return char