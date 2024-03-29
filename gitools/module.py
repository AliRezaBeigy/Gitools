import re
import sys
import subprocess
from os import path
from typing import List
from shutil import rmtree, move
from .utils.editor import Editor
from .utils.utilities import Utilities
from .utils.option_selector import OptionSelector


class Module:
    def __init__(
        self,
        commit_hash,
        commit_date,
        author_name,
        commit_count,
        author_email,
        commit_message,
    ):
        if commit_count is None:
            commit_count = self.getDefaultCommitCount()

        self.commits = []
        self.commit_hash = commit_hash
        self.commit_date = commit_date
        self.author_name = author_name
        self.author_email = author_email
        self.commit_count = commit_count
        self.commit_message = commit_message

    @staticmethod
    def getFlag():
        raise NotImplementedError("getFlag isn't implemented")

    @staticmethod
    def getName():
        raise NotImplementedError("getName isn't implemented")

    @staticmethod
    def getDescription():
        raise NotImplementedError("getDescription isn't implemented")

    def isVisible(self):
        raise NotImplementedError("isVisible isn't implemented")

    def process(self):
        raise NotImplementedError("process isn't implemented")

    def selectCommit(self):
        if not self.commit_hash:
            self.commits = self.getCommits()
            header = "{:30s} {:30s} {:30s}".format("Author", "Message", "Date")

            options: List[str] = []
            for c in self.commits:
                options.append(
                    "{:30s} {:30s} {:30s}".format(
                        Utilities.ellipsis(c[2], 29),
                        Utilities.ellipsis(c[5], 29),
                        Utilities.ellipsis(c[4], 30),
                    )
                )

            index = OptionSelector(options, 0, header).getOption()
            self.commit_hash = self.commits[int(index)][0]

    def getCommits(self):
        out, err = self.excuteCommand("git log -n " + str(self.commit_count))

        if err:
            raise Exception("An Error Occurred:\r\n" + err.decode("utf-8"))

        out = out.decode("utf-8")

        commits = re.findall(
            r"commit\s([a-zA-Z0-9]*)(.*)\nAuthor:\s*([^<]*)<(.*)>\nDate:\s*(.*)\n\n(.*\n{0,1}.*)",
            out,
        )

        return [c[:-1] + (c[5].replace("    ", ""),) for c in commits]

    def getDefaultCommitCount(self):
        return min(500, int(self.excuteCommand("git rev-list --count HEAD")[0]))

    @staticmethod
    def runGC():
        Module.excuteCommand("git gc")

    @staticmethod
    def hasBackup():
        return path.exists(path.join(Utilities.cwd, ".git", "refs", "original"))

    @staticmethod
    def checkBackup():
        if Module.hasBackup():
            print("Are you sure you want to overwrite backup? [Default=Y/N]")
            res = input()
            if res.lower() == "n":

                print("Do you want to restore backup? [Y/Default=N]")
                res = input()
                if res.lower() == "y":
                    Module.restoreBackup()
                else:
                    sys.exit(1)

            else:
                Module.deleteBackup()

    @staticmethod
    def input(*argv):
        return Editor.input(*argv)

    @staticmethod
    def deleteBackup():
        rmtree(path.join(Utilities.cwd, ".git", "refs", "original"))

    @staticmethod
    def restoreBackup():
        rmtree(path.join(Utilities.cwd, ".git", "refs", "heads"))
        move(
            path.join(Utilities.cwd, ".git", "refs", "original", "refs", "heads"),
            path.join(Utilities.cwd, ".git", "refs"),
        )
        Module.deleteBackup()

    @staticmethod
    def excuteCommand(command):
        process = subprocess.Popen(
            Utilities.findShell(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Utilities.cwd,
        )

        return process.communicate(str.encode(command))
