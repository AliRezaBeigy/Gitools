from datetime import datetime
from ..module import Module


class UpdateDateModule(Module):
    def process(self):
        self.checkBackup()
        self.selectCommit()

        if not self.commit_date:
            old_commit_date = next(
                (commit for commit in self.commits if commit[0] == self.commit_hash),
                None,
            )
            date = self.input(
                "Fri Jan 1 00:00:00 2021 +0000"
                if old_commit_date is None
                else old_commit_date[4]
            )
            try:
                self.commit_date = datetime.strptime(
                    date, "%a %b %d %X %Y %z"
                ).strftime("%a %b %d %X %Y %z")
            except:
                pass

        try:
            self.commit_date = datetime.strptime(
                self.commit_date, "%a %b %d %X %Y %z"
            ).strftime("%a %b %d %X %Y %z")
        except:
            print('Enter Valid Date Such As "Fri Jan 1 00:00:00 2021 +0000"')
            self.process()
            return

        command = """git filter-branch -f --env-filter 'if [ $GIT_COMMIT = "COMMIT_HASH" ]
                then
                    export GIT_AUTHOR_DATE="NEW_DATE";
                    export GIT_COMMITTER_DATE="NEW_DATE";
                fi'""".replace(
            "COMMIT_HASH", self.commit_hash
        ).replace(
            "NEW_DATE", self.commit_date
        )

        _, err = self.excuteCommand(command)

        if not err:
            print("Date Changed Successfully")
        else:
            print("Date Change Failed, Error:\r\n" + err.decode("utf-8"))

    def getFlag():
        return "ud"

    def getName():
        return "Update Date"

    def getDescription():
        return "Update commit date time"

    def isVisible(self):
        return True
