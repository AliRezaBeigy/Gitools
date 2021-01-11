import re
import sys
from os import path
from datetime import datetime
from shutil import rmtree, move
from gitools.editor import Editor
from gitools.utils import Utilities


class Gitools:
    def __init__(self, commit_hash, commit_count, commit_date, commit_message,
                 author_name, author_email):
        if (commit_count is None):
            commit_count = 10

        self.commits = []
        self.commit_hash = commit_hash
        self.commit_date = commit_date
        self.author_name = author_name
        self.author_email = author_email
        self.commit_count = commit_count
        self.commit_message = commit_message

    def updateDate(self):
        self.checkBackup()
        self.selectCommit()

        if not self.commit_date:
            date = input('Enter New Commit Date: ')
            try:
                self.commit_date = datetime.strptime(
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
                fi'""".replace("COMMIT_HASH", self.commit_hash).replace(
            "NEW_DATE", self.commit_date)

        _, err = Utilities.excuteCommand(command)

        if not err:
            print("Date Changed Successfully")
        else:
            print("Date Change Failed, Error:\r\n" + err.decode('utf-8'))

    def updateMessage(self):
        self.checkBackup()
        self.selectCommit()

        if not self.commit_message:
            old_message = next(
                (commit
                 for commit in self.commits if commit[0] == self.commit_hash),
                None)
            self.commit_message = Editor.input(
                '# Enter New Commit Message'
                if old_message is None else old_message[5])

        command = """git filter-branch --msg-filter 'if [[ $GIT_COMMIT = "COMMIT_HASH" ]]
                    then
                        echo "NEW_MESSAGE"
                    else
                        cat
                    fi'""".replace("COMMIT_HASH", self.commit_hash).replace(
            "NEW_MESSAGE", self.commit_message)

        _, err = Utilities.excuteCommand(command)

        if not err:
            print("Commit Message Changed Successfully")
        else:
            print("Commit Message Change Failed, Error:\r\n" +
                  err.decode('utf-8'))

    def updateAuthor(self):
        self.checkBackup()
        self.selectCommit()

        if not self.author_name:
            self.author_name = input('Enter New Author Name: ').strip()
        if not self.author_email:
            self.author_email = input('Enter New Author Email: ').strip()

        print()

        command = """git filter-branch --env-filter 'if [[ $GIT_COMMIT = "COMMIT_HASH" ]]
                    then
                        export GIT_AUTHOR_NAME="NEW_AUTHOR_NAME"
                        export GIT_AUTHOR_EMAIL="NEW_AUTHOR_EMAIL"
                        export GIT_COMMITTER_NAME="NEW_AUTHOR_NAME"
                        export GIT_COMMITTER_EMAIL="NEW_AUTHOR_EMAIL"
                    fi'""".replace("COMMIT_HASH", self.commit_hash).replace(
            "NEW_AUTHOR_NAME",
            self.author_name).replace("NEW_AUTHOR_EMAIL", self.author_email)

        _, err = Utilities.excuteCommand(command)

        if not err:
            print("Commit Author Changed Successfully")
        else:
            print("Commit Author Change Failed, Error:\r\n" +
                  err.decode('utf-8'))

    def selectCommit(self):
        if not self.commit_hash:
            self.commits = self.getCommits()
            print('{:15s} {:30s} {:30s} {:30s}'.format('Index', 'Author',
                                                       'Message', 'Date'))
            for i, c in enumerate(self.commits):
                print('{:15s} {:30s} {:30s} {:30s}'.format(
                    str(i + 1), c[2], c[5], c[4]))

            print()
            index = input('Enter Commit Index: ')
            try:
                self.commit_hash = self.commits[int(index) - 1][0]
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
        if path.exists(path.join(Utilities.cwd, '.git', 'refs', 'original')):
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
        rmtree(path.join(Utilities.cwd, '.git', 'refs', 'original'))

    def restoreBackup(self):
        rmtree(path.join(Utilities.cwd, '.git', 'refs', 'heads'))
        move(
            path.join(Utilities.cwd, '.git', 'refs', 'original', 'refs',
                      'heads'), path.join(Utilities.cwd, '.git', 'refs'))
        self.deleteBackup()
