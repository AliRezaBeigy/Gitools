import os
import subprocess


class Utilities:
    cwd = os.getcwd()

    @staticmethod
    def findShell():
        try:
            process = subprocess.Popen(
                'bash',
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
            _, err = process.communicate()
            if not err:
                return 'bash'
        except:
            pass

        try:
            process = subprocess.Popen(
                'sh',
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
            _, err = process.communicate()
            if not err:
                return 'sh'
        except:
            pass

        try:
            process = subprocess.Popen(
                'where git',
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
            )
            out, err = process.communicate()
            if not err:
                out = out.decode('utf-8')
                out = out.split('\n')[0].strip()
                out = os.path.dirname(out)
                shellPath = os.path.join(out, '..', 'usr', 'bin', 'bash.exe')
                if os.path.exists(shellPath):
                    return os.path.abspath(shellPath)
                shellPath = os.path.join(out, '..', 'usr', 'bin', 'sh.exe')
                if os.path.exists(shellPath):
                    return os.path.abspath(shellPath)
        except:
            pass

    @staticmethod
    def excuteCommand(command):
        process = subprocess.Popen(Utilities.findShell(),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=Utilities.cwd)

        return process.communicate(str.encode(command))

    @staticmethod
    def clearConsole():
        os.system('cls' if os.name == 'nt' else 'clear')
