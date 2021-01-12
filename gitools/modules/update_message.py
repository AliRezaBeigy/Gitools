from gitools.module import Module


class UpdateMessageModule(Module):
    def process(self):
        self.checkBackup()
        self.selectCommit()

        if not self.commit_message:
            old_message = next(
                (commit for commit in self.commits if commit[0] == self.commit_hash),
                None,
            )
            self.commit_message = self.input(
                "# Enter New Commit Message" if old_message is None else old_message[5]
            )

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

        if not err:
            print("Commit Message Changed Successfully")
        else:
            print("Commit Message Change Failed, Error:\r\n" + err.decode("utf-8"))

    def getFlag():
        return "um"

    def getName():
        return "Update Message"

    def getDescription():
        return "Update commit message"

    def isVisible(self):
        return True
