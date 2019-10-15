import threading
from abc import ABCMeta, abstractmethod

class Thread(object):
    def __init__(self):
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    @abstractmethod
    def run(self):
        pass
