from model.Connection import Connection
from model.Server import Server
from model.udp.UdpSocket import UdpSocket


class UdpServer(Server):
    def __init__(self, server_address, storage_dir):
        super().__init__(storage_dir)
        self.server_socket = UdpSocket(server_address)
        self.server_socket.bind_and_listen()
        self.connect_with_client()

    def connect_with_client(self):
        connection: Connection = Connection(self.server_socket)
        super().new_connection(connection)

    def reset(self):
        # reseteo el conn_address
        self.server_socket.connect()
