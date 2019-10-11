
import threading
import socket

from udp.RudpSocket import RudpSocket


class UdpServer(object):
    CHUNK_SIZE = 1024
    UPLOAD_MODE = 'upload'
    DOWNLOAD_MODE = 'download'

    def __init__(self):
        self.keep_running = True
        self.thread = None
        self.sock = None
        self.ended = False

    def start(self, server_address, storage_dir):
        self.keep_running = True
        self.thread = threading.Thread(target=self.run,
                                       args=(server_address, storage_dir))
        self.thread.start()

    def stop(self):
        self.keep_running = False
        try:
            self.sock.shutdown(socket.SHUT_RD)
        except:
            pass
        self.thread.join()

    def run(self, server_address, storage_dir):
        self.sock = RudpSocket()
        self.sock.bind(server_address)

        while self.keep_running:
            mode, addr = self.sock.recvfrom(self.CHUNK_SIZE)
            if mode == self.UPLOAD_MODE:
                self.upload_file(addr, storage_dir)
            elif mode == self.DOWNLOAD_MODE:
                self.download_file()

        self.ended = True

    def upload_file(self, addr, storage_dir):
        name, addr = self.sock.recvfrom(self.CHUNK_SIZE)
        size, addr = self.sock.recvfrom(self.CHUNK_SIZE)

        filepath = '{}/{}'.format(storage_dir, name)

        with open(filepath, 'wb') as file:
            bytes_received = 0
            while bytes_received < size:
                chunk, addr = self.sock.recvfrom(self.CHUNK_SIZE)
                bytes_received += len(chunk)
                file.write(chunk)


    def download_file(self):
        pass