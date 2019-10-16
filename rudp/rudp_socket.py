import queue
import socket
from rudp.scheduler import Scheduler

class RudpSocket(object):
    def __init__(self, own_addr):
        self.own_addr = own_addr
        self.init_socket()
        self.scheduler = Scheduler()
        self.start_services()

    def start_services(self):
        self.scheduler.start()

    def close_services(self):
        self.scheduler.stop()
        self.scheduler.join()

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.own_addr)

    def sendto(self, data, addr):
        return self.sock.sendto(data, addr)

    def recvfrom(self, bufsize):
        return self.sock.recvfrom(bufsize)

    def close(self):
        self.close_services()
        self.sock.close()
