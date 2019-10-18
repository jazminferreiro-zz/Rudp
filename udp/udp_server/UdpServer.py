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
                self.upload_file(storage_dir, connection)
            elif mode == 'download':
                self.download_file(addr, storage_dir, connection)
            else:
                print('Invalid mode')
        connection.close()

    def upload_file(self, storage_dir, connection):
        connection.recv_file(storage_dir)

    def download_file(self, addr, storage_dir, connection):
        name, addr = connection.recvfrom()
        pathname = '{}/{}'.format(storage_dir, name)
        connection.send_file(pathname, name, addr)
