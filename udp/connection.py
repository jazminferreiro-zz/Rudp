from rudp.rudp_socket import RudpSocket
import os

class Connection(object):
    BUFSIZE = 1024

    def __init__(self, addr):
        self.sock = RudpSocket(addr)

    def close(self):
        self.sock.close()

    def send_file(self, src, name, server_address):
        self.sock.sendto(name, server_address)

    def recv_file(self, addr, storage_dir):
        self.sock.recvfrom(self.BUFSIZE)
        pass

    def sendto(self, data, addr):
        self.sock.sendto(data, addr)

    def recvfrom(self):
        return self.sock.recvfrom(1024)

    def file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size
