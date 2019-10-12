import os

from udp.RudpSocket import RudpSocket


class UdpClient(object):
    UPLOAD_MODE = 'upload'
    DOWNLOAD_MODE = 'download'
    CHUNK_SIZE = 1024
    OWN_ADDR = ('127.0.0.1', 8888)
    SUCCESS = 0
    ERROR = -1

    def file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size

    def upload(self, server_address, src, name):
        sock = RudpSocket()
        sock.bind(self.OWN_ADDR)

        sock.sendto(self.UPLOAD_MODE, server_address)
        sock.sendto(name, server_address)

        with open(src, 'rb') as file:
            sock.sendto(self.file_size(file), server_address)

            while True:
                chunk = file.read(int(self.CHUNK_SIZE/2))
                if not chunk:
                    break
                sock.sendto(chunk, server_address)

    def download(self, server_address, name, dest):
        sock = RudpSocket()
        sock.bind(self.OWN_ADDR)

        sock.sendto(self.DOWNLOAD_MODE, server_address)
        sock.sendto(name, server_address)

        size, server_address = sock.recvfrom(self.CHUNK_SIZE)
        with open(dest, 'wb') as file:
            bytes_received = 0
            while bytes_received < size:
                chunk, server_address = sock.recvfrom(self.CHUNK_SIZE)
                bytes_received += len(chunk)
                file.write(chunk)






