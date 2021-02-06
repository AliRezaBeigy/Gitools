from ..module import Module


class RestoreBackupModule(Module):
    def process(self):
        Module.restoreBackup()

    @staticmethod
    def getFlag():
        return "rb"

    @staticmethod
    def getName():
        return "Restore Backup"

    @staticmethod
    def getDescription():
        return ""

    def isVisible(self):
        return Module.hasBackup()
