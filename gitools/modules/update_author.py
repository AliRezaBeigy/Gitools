from gitools.module import Module


class UpdateAuthorModule(Module):
    def process(self):
        self.checkBackup()
        self.selectCommit()

        if not self.author_name:
            self.author_name = input("Enter New Author Name: ").strip()
        if not self.author_email:
            self.author_email = input("Enter New Author Email: ").strip()

        print()

        command = (
            """git filter-branch --env-filter 'if [[ $GIT_COMMIT = "COMMIT_HASH" ]]
                    then
                        export GIT_AUTHOR_NAME="NEW_AUTHOR_NAME"
                        export GIT_AUTHOR_EMAIL="NEW_AUTHOR_EMAIL"
                        export GIT_COMMITTER_NAME="NEW_AUTHOR_NAME"
                        export GIT_COMMITTER_EMAIL="NEW_AUTHOR_EMAIL"
                    fi'""".replace(
                "COMMIT_HASH", self.commit_hash
            )
            .replace("NEW_AUTHOR_NAME", self.author_name)
            .replace("NEW_AUTHOR_EMAIL", self.author_email)
        )

        _, err = self.excuteCommand(command)

        if not err:
            print("Commit Author Changed Successfully")
        else:
            print("Commit Author Change Failed, Error:\r\n" + err.decode("utf-8"))

    def getFlag():
        return "ua"

    def getName():
        return "Update Author"

    def getDescription():
        return "Update author information"

    def isVisible(self):
        return True
