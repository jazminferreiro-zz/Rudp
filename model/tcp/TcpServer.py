from model.Connection import Connection
from model.Server import Server
from model.tcp.TcpSocket import TcpSocket


class TcpServer(Server):
    def __init__(self, server_address, storage_dir):
        super().__init__(storage_dir)
        self.connection = None
        self.server_socket = TcpSocket(server_address)
        self.server_socket.bind_and_listen()



    def connect_with_client(self):
        try:
            socket = self.server_socket.accept()
            connection = Connection(socket)
            self.connection = connection
            super().new_connection(self.connection)
        except OSError:
            print("Se cerro el server socket")


    def stop_running(self, **kwargs):
        self.server_socket.stop()
        super().stop_running(self.connection)


