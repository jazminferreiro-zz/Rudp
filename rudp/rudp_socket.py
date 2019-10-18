import queue
import socket
import time
from rudp.scheduler import Scheduler
from rudp.sender import Sender
from rudp.receiver import Receiver
from rudp.arranger import Arranger

class RudpSocket(object):
    WAIT_LAST_ACK_SECONDS = 0.5

    def __init__(self, addr):
        self.addr = addr
        self.sock = self.create_socket(self.addr)
        self.queue = queue.Queue()
        self.sender = Sender(self.sock)
        self.scheduler = Scheduler(self.sender)
        self.arranger = Arranger(self.queue)
        self.receiver = Receiver(self.sock, self.sender, self.scheduler, self.arranger)
        self.start_services()

    def start_services(self):
        self.sender.start()
        self.scheduler.start()
        self.arranger.start()
        self.receiver.start()

    def close_services(self):
        self.scheduler.stop()
        self.scheduler.join()
        self.sender.stop()
        self.sender.join()
        self.receiver.stop()
        self.receiver.join()
        self.arranger.stop()
        self.arranger.join()

    def create_socket(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr)
        return sock

    def sendto(self, data, dst_addr):
        pack = {
            'header': {
                    'src_addr': self.addr,
                    'dst_addr': dst_addr
            },
            'payload': data
        }
        self.scheduler.put(pack)

    def recvfrom(self, bufsize):
        pack = self.queue.get()
        self.queue.task_done()
        return pack.get('payload'), pack.get('header').get('src_addr')

    def wait_last_ack(self):
        time.sleep(self.WAIT_LAST_ACK_SECONDS)

    def close(self):
        self.wait_last_ack()
        self.queue.join()
        self.close_services()
        self.sock.close()
