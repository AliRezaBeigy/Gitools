import argparse
from os import path
from gitools.utils import Utilities
from gitools.gitools import Gitools


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c",
                            "--count",
                            type=int,
                            required=False,
                            help="number of commit to show")
        parser.add_argument("-ae",
                            "--author-email",
                            type=str,
                            required=False,
                            help="author email")
        parser.add_argument("-an",
                            "--author-name",
                            type=str,
                            required=False,
                            help="author name")
        parser.add_argument("-cd",
                            "--commit-date",
                            type=int,
                            required=False,
                            help="commit date")
        parser.add_argument("-ch",
                            "--commit-hash",
                            type=str,
                            required=False,
                            help="commit hash")
        parser.add_argument("-cm",
                            "--commit-message",
                            type=str,
                            required=False,
                            help="commit message")
        parser.add_argument("-m",
                            "--mode",
                            type=str,
                            required=False,
                            help='command mode')
        parser.add_argument("-i",
                            "--input",
                            type=str,
                            required=False,
                            help="git directory")
        args = parser.parse_args()

        selectMode(args)

        if args.input:
            Utilities.cwd = path.realpath(args.input)

        gitHand = Gitools(commit_count=args.count,
                          commit_hash=args.commit_hash,
                          commit_date=args.commit_date,
                          author_name=args.author_name,
                          author_email=args.author_email,
                          commit_message=args.commit_message)
        if args.mode == 'ud':
            gitHand.updateDate()
        elif args.mode == 'um':
            gitHand.updateMessage()
        elif args.mode == 'ua':
            gitHand.updateAuthor()
        elif args.mode == 'rb':
            gitHand.restoreBackup()
        else:
            parser.print_help()
        pass
    except KeyboardInterrupt:
        print()
        print('Process Canceled')


def selectMode(args):
    modes = [('Update Date', 'ud', 'Update commit date time'),
             ('Update Message', 'um', 'Update commit message'),
             ('Update Author', 'ua', 'Update author information'),
             ('Restore Backup', 'rb', 'Restore Backup')]
    if not args.mode:
        print('{:15s} {:25s} {:10s} {:30s}'.format('Index', 'Mode', 'Flag',
                                                   'Description'))
        for i, mode in enumerate(modes):
            print('{:15s} {:25s} {:10s} {:30s}'.format(*((str(i + 1), ) +
                                                         mode)))
        index = input("Enter Mode Index: ")
        try:
            args.mode = modes[int(index) - 1][1]
            Utilities.clearConsole()
        except:
            Utilities.clearConsole()
            print(
                "Enter a valid index or run with like following command\r\n> gitools -m uh"
            )
            print()
            selectMode(args)


if __name__ == "__main__":
    main()