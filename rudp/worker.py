import pickle
import threading
from rudp.sender import Sender

class Worker(object):
    TIMEOUT = 0.3

    def __init__(self, pack, sender):
        self.pack = pack
        self.sender = sender
        self.arrived_ack_event = threading.Event()
        self.arrived_ack = False

    def run(self):
        print('-- init worker')
        while not self.arrived_ack:
            print('-- worker sending package: ', self.pack)
            self.sender.put(self.pack)
            self.arrived_ack_event.wait(self.TIMEOUT)
        print('-- end worker')

    def stop(self):
        print('-- worker stopping, setting event()')
        self.arrived_ack = True
        self.arrived_ack_event.set()
