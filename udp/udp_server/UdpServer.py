from udp.connection import Connection
import time
import os

class UdpServer(object):
    BUFSIZE = 1024

    def run(self, server_address, storage_dir):
        while True:
            connection = Connection(server_address)
            print('-- waiting mode or ctrl+z to stop...')

            mode, addr = connection.recvfrom()
            if mode == 'upload':
                self.upload_file(storage_dir, connection)
            elif mode == 'download':
                self.download_file(addr, storage_dir, connection)
            else:
                print('Invalid mode')

            connection.wait_last_ack()
            connection.close()
            print('-- end')

    def upload_file(self, storage_dir, connection):
        self.create_dir(storage_dir)
        name, addr = connection.recvfrom()
        pathname = '{}/{}'.format(storage_dir, name)
        connection.recv_file(pathname)

    def download_file(self, addr, storage_dir, connection):
        name, addr = connection.recvfrom()
        pathname = '{}/{}'.format(storage_dir, name)
        connection.send_file(pathname, addr)

    def create_dir(self, dir):
        """ Validación de directorio, si no existe lo crea. """
        if not os.path.exists(dir):
            os.mkdir(dir)
            print('Dir: {} created!'.format(dir))
