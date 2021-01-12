import argparse
from os import path
from gitools.module import Module
from gitools.utils.utilities import Utilities
from gitools.modules.update_date import UpdateDateModule
from gitools.modules.update_author import UpdateAuthorModule
from gitools.modules.update_message import UpdateMessageModule
from gitools.modules.restore_backup import RestoreBackupModule

modules: list[Module] = [
    UpdateDateModule,
    UpdateAuthorModule,
    UpdateMessageModule,
    RestoreBackupModule,
]


def main():
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
        print(
            "{:15s} {:25s} {:10s} {:30s}".format(
                "Index", "Module", "Flag", "Description"
            )
        )

        for i, m in enumerate(modules):
            module.__class__ = m
            if module.isVisible():
                print(
                    "{:15s} {:25s} {:10s} {:30s}".format(
                        str(i + 1),
                        m.getName(),
                        m.getFlag(),
                        m.getDescription(),
                    )
                )
        module.__class__ = Module

        index = input("Enter Module Index: ")
        try:
            args.module = modules[int(index) - 1].getFlag()
            Utilities.clearConsole()
        except:
            Utilities.clearConsole()
            print(
                "Enter a valid index or run with like following command\r\n> gitools -m uh"
            )
            print()
            selectModule(args)


if __name__ == "__main__":
    main()