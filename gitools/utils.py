import os
import subprocess


class Utilities:
    @staticmethod
    def findShell():
        try:
            process = subprocess.Popen(
                'bash',
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
            )
            out, err = process.communicate()

            if not err:
                return 'bash'
        except:
            pass

        try:
            process = subprocess.Popen(
                'sh',
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
            )
            out, err = process.communicate()

            if not err:
                return 'sh'
        except:
            pass

        try:
            process = subprocess.Popen(
                'where git',
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
            )
            out, err = process.communicate()

            if not err:
                out = out.decode('utf-8')
                return next(x for x in out.split('\n')
                            if '\\cmd\\git.exe' in x).strip().replace(
                                "cmd\\git.exe", "bin\\bash.exe")
        except:
            pass

    @staticmethod
    def excuteCommand(command):
        process = subprocess.Popen(
            Utilities.findShell(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # TODO Remove Following Arg
            cwd=os.getcwd())

        return process.communicate(str.encode(command))

    @staticmethod
    def clearConsole():
        os.system('cls' if os.name == 'nt' else 'clear')
