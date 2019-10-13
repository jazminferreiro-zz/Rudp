from model.Client import Client
from model.Connection import Connection
from model.tcp.TcpSocket import TcpSocket


class TcpClient(Client):
    def __init__(self, server_address):
        socket = TcpSocket(server_address)
        socket.connect()
        connection = Connection(socket)
        super().__init__(connection)