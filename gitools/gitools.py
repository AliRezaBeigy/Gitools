import re
import os
import sys
from datetime import datetime
from gitools.utils import Utilities
from gitools.getChar import readChar


class Gitools:
    def __init__(self, hash, commit_count, date):
        if (commit_count is None):
            commit_count = 10

        self.hash = hash
        self.date = date
        self.new_message = None
        self.commit_count = commit_count

    def updateDate(self):
        self.checkBackup()
        self.selectCommit()

        if not self.date:
            date = input('Enter New Commit Date: ')
            try:
                self.date = datetime.strptime(
                    date, '%a %b %d %X %Y %z').strftime('%a %b %d %X %Y %z')
            except:
                print(
                    'Enter Valid Date Such As "Fri Jan 1 00:00:00 2021 +0000"')
                self.updateDate()
                return

        command = """git filter-branch -f --env-filter 'if [ $GIT_COMMIT = "COMMIT_HASH" ]
                then
                    export GIT_AUTHOR_DATE="NEW_DATE";
                    export GIT_COMMITTER_DATE="NEW_DATE";
                fi'""".replace("COMMIT_HASH",
                               self.hash).replace("NEW_DATE", self.date)

        _, err = Utilities.excuteCommand(command)

        if not err:
            print("Date Changed Successfully")
        else:
            print("Date Change Failed")

    def updateMessage(self):
        self.checkBackup()
        self.selectCommit()

        if not self.new_message:
            print('Enter New Commit Message (Press Ctrl-C once to save):')
            new_message = ''
            while True:
                c = readChar()
                if c == '\x08':
                    new_message = new_message[:-1]
                elif c == '\x03':
                    break
                else:
                    new_message = new_message + c
            self.new_message = new_message.strip()

        print()

        command = """git filter-branch --msg-filter 'if [[ $GIT_COMMIT = "COMMIT_HASH" ]]
                    then
                        echo "NEW_MESSAGE"
                    else
                        cat
                    fi'""".replace("COMMIT_HASH",
                                   self.hash).replace("NEW_MESSAGE",
                                                      self.new_message)

        _, err = Utilities.excuteCommand(command)

        if not err:
            print("Commit Message Changed Successfully")
        else:
            print("Commit Message Change Failed")

    def selectCommit(self):
        if not self.hash:
            commits = self.getCommits()
            print('{:15s} {:30s} {:30s} {:30s}'.format('Index', 'Author',
                                                       'Message', 'Date'))
            for i, c in enumerate(commits):
                print('{:15s} {:30s} {:30s} {:30s}'.format(
                    str(i + 1), c[2], c[5], c[4]))

            print()
            index = input('Enter Commit Index: ')
            try:
                self.hash = commits[int(index) - 1][0]
                print()
            except:
                Utilities.clearConsole()
                print(
                    "Enter a valid index or run with like following command\r\n> gitools --hash xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                )
                print()
                self.selectCommit()

    def getCommits(self):
        out, err = Utilities.excuteCommand('git log -n ' +
                                           str(self.commit_count))

        if err:
            raise Exception("An Error Occurred:\r\n" + err.decode("utf-8"))

        out = out.decode("utf-8")

        return re.findall(
            r'commit\s([a-zA-Z0-9]*)(.*)\nAuthor:\s*([^<]*)<(.*)>\nDate:\s*(.*)\n\n\s*(.*)',
            out)

    def checkBackup(self):
        if os.path.exists('.git/refs/original'):
            print('Are you sure you want to overwrite backup? [Default=Y/N]')
            res = input()
            if res.lower() == 'n':

                print('Do you want to restore backup? [Y/Default=N]')
                res = input()
                if res.lower() == 'y':
                    self.restoreBackup()
                else:
                    sys.exit(1)

            else:
                self.deleteBackup()

    def deleteBackup(self):
        Utilities.excuteCommand('rm -rf .git/refs/original')

    def restoreBackup(self):
        Utilities.excuteCommand(
            'rm -rf .git/refs/heads '
            '&& mv .git/refs/original/refs/heads .git/refs')
        self.deleteBackup()
