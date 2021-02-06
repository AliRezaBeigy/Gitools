import re
import sys
import subprocess
from os import path
from typing import List
from shutil import rmtree, move
from .utils.editor import Editor
from .utils.utilities import Utilities
from abc import ABCMeta, abstractmethod
from .utils.option_selector import OptionSelector


class Module:
    __metaclass__ = ABCMeta

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
            commit_count = 10

        self.commits = []
        self.commit_hash = commit_hash
        self.commit_date = commit_date
        self.author_name = author_name
        self.author_email = author_email
        self.commit_count = commit_count
        self.commit_message = commit_message

    @staticmethod
    @abstractmethod
    def getFlag():
        raise NotImplementedError("getFlag isn't implemented")

    @staticmethod
    @abstractmethod
    def getName():
        raise NotImplementedError("getName isn't implemented")

    @staticmethod
    @abstractmethod
    def getDescription():
        raise NotImplementedError("getDescription isn't implemented")

    @abstractmethod
    def isVisible(self):
        raise NotImplementedError("isVisible isn't implemented")

    @abstractmethod
    def process(self):
        raise NotImplementedError("process isn't implemented")

    def selectCommit(self):
        if not self.commit_hash:
            self.commits = self.getCommits()
            header = "{:30s} {:30s} {:30s}".format("Author", "Message", "Date")

            options: List[str] = []
            for i, c in enumerate(self.commits):
                options.append("{:30s} {:30s} {:30s}".format(c[2], c[5], c[4]))

            index = OptionSelector(options, 0, header).getOption()
            self.commit_hash = self.commits[int(index)][0]

    def getCommits(self):
        out, err = self.excuteCommand("git log -n " + str(self.commit_count))

        if err:
            raise Exception("An Error Occurred:\r\n" + err.decode("utf-8"))

        out = out.decode("utf-8")

        return re.findall(
            r"commit\s([a-zA-Z0-9]*)(.*)\nAuthor:\s*([^<]*)<(.*)>\nDate:\s*(.*)\n\n\s*(.*)",
            out,
        )

    def hasBackup(self):
        return path.exists(path.join(Utilities.cwd, ".git", "refs", "original"))

    def checkBackup(self):
        if self.hasBackup():
            print("Are you sure you want to overwrite backup? [Default=Y/N]")
            res = input()
            if res.lower() == "n":

                print("Do you want to restore backup? [Y/Default=N]")
                res = input()
                if res.lower() == "y":
                    self.restoreBackup()
                else:
                    sys.exit(1)

            else:
                self.deleteBackup()

    def input(self, *argv):
        return Editor.input(*argv)

    def deleteBackup(self):
        rmtree(path.join(Utilities.cwd, ".git", "refs", "original"))

    def restoreBackup(self):
        rmtree(path.join(Utilities.cwd, ".git", "refs", "heads"))
        move(
            path.join(Utilities.cwd, ".git", "refs", "original", "refs", "heads"),
            path.join(Utilities.cwd, ".git", "refs"),
        )
        self.deleteBackup()

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
