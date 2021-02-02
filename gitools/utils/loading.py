from multiprocessing import Process
from time import sleep


class Loading:
    message: str
    level: int = 0
    worker: Process
    max_level: int = 3

    def __init__(self, message):
        self.message = message
        self.worker = Process(target=self.printLoading)
        self.worker.start()

    def printLoading(self):
        print(
            " "
            + self.message
            + ("." * self.level)
            + (" " * (self.max_level - self.level)),
            end="\r",
        )
        sleep(1)
        self.level += 1
        if self.level > self.max_level:
            self.level = 0
        self.printLoading()

    def stop(self):
        self.worker.terminate()