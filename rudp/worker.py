import pickle
from rudp.sender import Sender

class Worker(object):
    def __init__(self, pack, sender):
        self.pack = pack
        self.sender = sender

    def run(self):
        print('-- init worker')
        print('-- worker: {}'.format(self.pack))
        print('-- worker sending package')
        self.sender.put(self.pack)
        print('-- end worker')
