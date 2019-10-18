from rudp.rudp_socket import RudpSocket
import os
import time

class Connection(object):
    # otherwise is too much for pickle (max dumped package: 4kB)
    BUFSIZE = 1024
    CHUNK_SIZE = int(BUFSIZE / 2)
    SUCESS = 0
    ERROR = -1
    WAIT_LAST_ACK_SECONDS = 1

    def __init__(self, addr):
        self.sock = RudpSocket(addr)

    def close(self):
        self.sock.close()

    def send_file(self, src, name, server_address):
        with open(src, 'rb') as file:
            self.sock.sendto(name, server_address)
            self.sock.sendto(self.file_size(file), server_address)

            while True:
                chunk = file.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                self.sock.sendto(chunk, server_address)

        bytes, addr = self.sock.recvfrom(self.BUFSIZE)
        return bytes


    def recv_file(self, storage_dir):
        name, addr = self.sock.recvfrom(self.BUFSIZE)
        size, addr = self.sock.recvfrom(self.BUFSIZE)
        pathfile = '{}/{}'.format(storage_dir, name)
        print(pathfile)

        with open(pathfile, 'wb') as file:
            bytes_recv = 0
            while bytes_recv < size:
                chunk, addr = self.sock.recvfrom(self.BUFSIZE)
                print(chunk)
                bytes_recv += len(chunk)
                file.write(chunk)

        self.sendto(bytes_recv, addr)

    def sendto(self, data, addr):
        self.sock.sendto(data, addr)

    def recvfrom(self):
        return self.sock.recvfrom(self.BUFSIZE)

    def wait_last_ack(self):
        time.sleep(self.WAIT_LAST_ACK_SECONDS)

    def file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size
