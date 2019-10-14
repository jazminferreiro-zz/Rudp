from model.Connection import Connection
from model.Server import Server
from model.udp.UdpSocket import UdpSocket


class UdpServer(Server):
    def __init__(self, server_address, storage_dir):
        super().__init__(storage_dir)
        self.connection = None
        self.server_socket = UdpSocket(server_address)
        self.server_socket.bind_and_listen()

    def connect_with_client(self):
        connection: Connection = Connection(self.server_socket)
        self.connection = connection
        super().new_connection(self.connection)

    def reset(self):
        # reseteo el conn_address y seq_num received
        self.server_socket.connect()

    def stop_running(self, **kwargs):
        self.server_socket.stop()
        super().stop_running(self.connection)
