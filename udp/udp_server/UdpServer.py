from udp.connection import Connection
import time

class UdpServer(object):
    BUFSIZE = 1024

    def run(self, server_address, storage_dir):
        connection = Connection(server_address)
        while True:

            print('-- waiting mode')
            mode, addr = connection.recvfrom()
            if mode == 'upload':
                self.upload_file(addr, storage_dir, connection)
        connection.close()

    def upload_file(self, addr, storage_dir, connection):
        connection.recv_file(addr, storage_dir)

    def download_file(self, addr, storage_dir, connection):
        pass
