import argparse
from typing import List
from os import path, _exit
from .module import Module
from .utils.editor import Editor
from .utils.utilities import Utilities
from .utils.option_selector import OptionSelector
from .modules.update_date import UpdateDateModule
from .modules.update_author import UpdateAuthorModule
from .modules.update_message import UpdateMessageModule
from .modules.restore_backup import RestoreBackupModule

modules: List[Module] = [
    UpdateDateModule,
    UpdateAuthorModule,
    UpdateMessageModule,
    RestoreBackupModule,
]


def main():
    checkRequirements()

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-c", "--count", type=int, required=False, help="number of commit to show"
        )
        parser.add_argument(
            "-ae", "--author-email", type=str, required=False, help="author email"
        )
        parser.add_argument(
            "-an", "--author-name", type=str, required=False, help="author name"
        )
        parser.add_argument(
            "-cd", "--commit-date", type=int, required=False, help="commit date"
        )
        parser.add_argument(
            "-ch", "--commit-hash", type=str, required=False, help="commit hash"
        )
        parser.add_argument(
            "-cm", "--commit-message", type=str, required=False, help="commit message"
        )
        parser.add_argument(
            "-i", "--input", type=str, required=False, help="git directory"
        )
        parser.add_argument(
            "-m",
            "--module",
            type=str,
            required=False,
            help="select module to do something",
        )
        args = parser.parse_args()

        if args.input:
            Utilities.cwd = path.realpath(args.input)

        while not path.exists(path.join(Utilities.cwd, ".git")):
            if path.ismount(Utilities.cwd):
                print(
                    "No '.git' folder found! Make sure you are in the repository folder."
                )
                exit()
            Utilities.cwd = path.realpath(path.join(Utilities.cwd, ".."))

        module = Module(
            commit_count=args.count,
            commit_hash=args.commit_hash,
            commit_date=args.commit_date,
            author_name=args.author_name,
            author_email=args.author_email,
            commit_message=args.commit_message,
        )

        selectModule(args, module)

        for m in modules:
            if args.module == m.getFlag():
                module.__class__ = m

        if module.__class__ == Module:
            parser.print_help()
            return

        module.process()
    except KeyboardInterrupt:
        print()
        print("Process Canceled")


def selectModule(args, module: Module):
    if not args.module:
        Utilities.clearConsole()
        header = "{:25s} {:10s} {:30s}".format("Module", "Flag", "Description")

        options: List[str] = []
        for m in modules:
            module.__class__ = m
            if module.isVisible():
                options.append(
                    "{:25s} {:10s} {:30s}".format(
                        Utilities.ellipsis(m.getName(), 24),
                        Utilities.ellipsis(m.getFlag(), 9),
                        Utilities.ellipsis(m.getDescription(), 29),
                    )
                )

        module.__class__ = Module

        index = OptionSelector(options, 0, header).getOption()

        try:
            args.module = modules[int(index)].getFlag()
            Utilities.clearConsole()
        except:
            Utilities.clearConsole()
            print(
                "Enter a valid index or run with like following command\r\n> gitools -m uh"
            )
            print()
            selectModule(args, module)


def checkRequirements():
    if not Utilities.gitExisted():
        print("There is no git to use :(\r\nplease install git then retry :D")
        _exit(1)
    if len(Utilities.findShell()) == 0:
        print("There is no shell application to use :(")
        _exit(1)
    if len(Editor.findEditor()) == 0:
        print(
            "There is no text editor to use :(\r\nplease install nano or vim then retry :D"
        )
        _exit(1)