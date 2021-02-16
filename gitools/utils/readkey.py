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
        import tty, termios, fcntl, os

    def __call__(self):
        import tty, termios, fcntl, os

        result = b""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            result += key.encode('utf-8')
            
            fd = sys.stdin.fileno()
            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)
            oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
            try:
                while key != '':
                    try:
                        key = sys.stdin.read(1)
                        result += key.encode('utf-8')
                    except IOError:
                        break
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return result


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