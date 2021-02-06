from ..module import Module
from ..utils.loading import Loading
from gitools.utils.utilities import Utilities


class UpdateMessageModule(Module):
    def process(self):
        Module.checkBackup()
        self.selectCommit()

        if not self.commit_message:
            old_message = next(
                (commit for commit in self.commits if commit[0] == self.commit_hash),
                None,
            )
            self.commit_message = Module.input(
                "# Enter New Commit Message" if old_message is None else old_message[5]
            ).replace("# Enter New Commit Message", "")

        Utilities.clearConsole()
        loading = Loading("Please wait")

        command = """git filter-branch --msg-filter 'if [[ $GIT_COMMIT = "COMMIT_HASH" ]]
                    then
                        echo "NEW_MESSAGE"
                    else
                        cat
                    fi'""".replace(
            "COMMIT_HASH", self.commit_hash
        ).replace(
            "NEW_MESSAGE", self.commit_message
        )

        _, err = self.excuteCommand(command)

        loading.stop()
        Utilities.clearConsole()

        if not err:
            print("Commit Message Changed Successfully")
        else:
            print("Commit Message Change Failed, Error:\r\n" + err.decode("utf-8"))

    @staticmethod
    def getFlag():
        return "um"

    @staticmethod
    def getName():
        return "Update Message"

    @staticmethod
    def getDescription():
        return "Update commit message"

    def isVisible(self):
        return True
