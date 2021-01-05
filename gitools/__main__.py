import argparse
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
        parser.add_argument("-d", "--date", type=int, required=False)
        parser.add_argument("-ch",
                            "--hash",
                            type=str,
                            required=False,
                            help="commit hash")
        parser.add_argument(
            "-m",
            "--mode",
            type=str,
            required=False,
        )
        args = parser.parse_args()

        selectMode(args)

        gitHand = Gitools(commit_count=args.count,
                          hash=args.hash,
                          date=args.date)
        if args.mode == 'ud':
            gitHand.updateDate()
        elif args.mode == 'um':
            gitHand.updateMessage()
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