import queue
import socket
from rudp.scheduler import Scheduler
from rudp.sender import Sender

class RudpSocket(object):
    def __init__(self, send_addr):
        self.send_addr = send_addr
        self.recv_addr = (send_addr[0], send_addr[1] + 1) # send_port + 1
        self.send_sock = self.create_socket(self.send_addr)
        self.recv_sock = self.create_socket(self.recv_addr)
        self.queue = queue.Queue()
        self.sender = Sender(self.send_sock)
        self.scheduler = Scheduler(self.sender)
        self.start_services()

    def start_services(self):
        self.sender.start()
        self.scheduler.start()


    def close_services(self):
        self.scheduler.stop()
        self.scheduler.join()
        self.sender.stop()
        self.sender.join()



    def create_socket(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr)
        return sock

    def sendto(self, data, dst_recv_addr):
        pack = {
            'header': {
                    'src_send_addr': self.send_addr,
                    'src_recv_addr': self.recv_addr,
                    'dst_recv_addr': dst_recv_addr
            },
            'payload': data
        }
        self.scheduler.put(pack)

    def recvfrom(self, bufsize):
        return self.recv_sock.recvfrom(bufsize)

    def close(self):
        self.queue.join()
        self.close_services()
        self.send_sock.close()
        self.recv_sock.close()
