import os
from rudp.rudp_socket import RudpSocket
import time

class UdpClient(object):
    UPLOAD_MODE = 'upload'
    DOWNLOAD_MODE = 'download'
    BUFSIZE = 512
    FILEBUSIZE = int(BUFSIZE/2)
    OWN_ADDR = ('127.0.0.1', 5000)

    def file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size

    def upload(self, server_address, src, name):
        print(server_address, src, name)
        sock = RudpSocket(self.OWN_ADDR)

        sock.sendto(self.UPLOAD_MODE, server_address)
        sock.sendto(name, server_address)

        with open(src, 'rb') as file:
            size = self.file_size(file)
            sock.sendto(size, server_address)

            while True:
                chunk = file.read(self.FILEBUSIZE)
                if not chunk:
                    break
                sock.sendto(chunk, server_address)

        data, addr = sock.recvfrom(self.BUFSIZE)
        print(data)
        sock.close()


    def download(self, server_address, name, dest):
        pass
