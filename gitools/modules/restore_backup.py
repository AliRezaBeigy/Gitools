from gitools.module import Module


class RestoreBackupModule(Module):
    def process(self):
        self.restoreBackup()

    def getFlag():
        return "rb"

    def getName():
        return "Restore Backup"

    def getDescription():
        return ""

    def isVisible(self):
        return self.hasBackup()
