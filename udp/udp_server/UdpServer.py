
import threading
import socket
import os
import time
from rudp.rudp_socket import RudpSocket

class UdpServer(object):
    BUFSIZE = 512
    FILEBUSIZE = int(BUFSIZE/2)
    UPLOAD_MODE = 'upload'
    DOWNLOAD_MODE = 'download'

    def file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size

    def run(self, server_address, storage_dir):
        while True:
            print('-- init socket')
            sock = RudpSocket(server_address)
            mode, addr = sock.recvfrom(self.BUFSIZE)

            if mode == self.UPLOAD_MODE:
                self.upload_file(addr, storage_dir, sock)
            else:
                self.download_file(addr, storage_dir, sock)

            sock.sendto('ok', addr)
            time.sleep(5)


    def upload_file(self, addr, storage_dir, sock):
        name, addr = sock.recvfrom(self.BUFSIZE)
        size, addr = sock.recvfrom(self.BUFSIZE)

        with open('{}/{}'.format(storage_dir, name), 'wb') as file:
            bytes_recv = 0
            while bytes_recv < size:
                chunk, addr = sock.recvfrom(self.BUFSIZE)
                bytes_recv += len(chunk)
                file.write(chunk)

        print(name, size)


    def download_file(self, addr, storage_dir, sock):
        pass
