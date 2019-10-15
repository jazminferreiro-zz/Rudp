from rudp.sender import Sender
from rudp.receiver import Receiver
from rudp.handler import Handler
import queue
import socket

class RudpSocket(object):
    def __init__(self, own_addr=('127.0.0.1', 9999)):
        self.own_addr = own_addr
        self.start_socket()
        self.queue = queue.Queue()
        self.sender = Sender(self.sock)
        self.handler = Handler(self.queue)
        self.receiver = Receiver(self.sock, self.handler, self.sender)
        self.start_services()

    def start_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.own_addr)

    def start_services(self):
        self.sender.start()
        self.handler.start()
        self.receiver.start()

    def sendto(self, data, addr):
        msg = {
            'header': {'src_addr': self.own_addr, 'dst_addr': addr, 'is_ack': False},
            'payload': data
        }
        self.sender.put(msg)

    def recvfrom(self, bufsize):
        data = self.queue.get()
        self.queue.task_done()
        return data.get('payload'), data.get('header').get('src_addr')

    def close(self):
        self.sender.wait_for_all_workers_to_stop()
        self.sender.stop()
        self.handler.stop()
        self.receiver.stop()
        print('rudp socket queue size', self.queue.qsize())
        self.queue.join()
