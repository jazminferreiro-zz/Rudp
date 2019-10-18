from udp.connection import Connection

class UdpServer(object):
    def run(self, server_address, storage_dir):
        while True:
            connection = Connection(server_address)

            print('-- waiting mode')
            mode, addr = connection.recvfrom()
            if mode == 'upload':
                self.upload_file(addr, storage_dir, connection)

            connection.close()

    def upload_file(self, addr, storage_dir, connection):
        connection.recv_file(addr, storage_dir)

    def download_file(self, addr, storage_dir, connection):
        pass
