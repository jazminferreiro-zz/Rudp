from rudp.thread import Thread
import pickle
import threading

class Worker(object):
    BUFSIZE = 1024
    TIMEOUT = 5

    def __init__(self, msg, sock):
        super().__init__()
        self.msg = msg
        self.sock = sock
        self.event = threading.Event()
        self.is_data_acknowledged = False

    def run(self):
        while not self.is_data_acknowledged:
            print('worker: ', self.msg.get('payload'),
                  ' is data ack?:', self.is_data_acknowledged)
            self.sock.sendto(pickle.dumps(self.msg), self.msg['header']['dst_addr'])
            self.event.wait(self.TIMEOUT)
        return 'FIN WORKER END OF WHILE'


    def data_is_acknowledge(self):
        self.is_data_acknowledged = True
        print('worker: data is acknowledged ', self.is_data_acknowledged)
        self.event.set()
