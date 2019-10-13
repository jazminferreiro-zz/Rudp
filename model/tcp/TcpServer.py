from model.Connection import Connection
from model.Server import Server
from model.tcp.TcpSocket import TcpSocket


class TcpServer(Server):
    def __init__(self, server_address, storage_dir):
        super().__init__(storage_dir)
        self.server_socket = TcpSocket(server_address)
        self.server_socket.bind_and_listen()
        self.connect_with_client()

    def connect_with_client(self):
        socket = self.server_socket.accept()
        connection = Connection(socket)
        super().new_connection(connection)
