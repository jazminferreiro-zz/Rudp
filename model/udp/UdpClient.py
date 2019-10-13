from model.Client import Client
from model.Connection import Connection
from model.udp.UdpSocket import UdpSocket


class UdpClient(Client):
    CLIENT_ADDR = ('127.0.0.1', 8888)
    def __init__(self, server_address):
        socket = UdpSocket(self.CLIENT_ADDR)
        socket.connect(server_address)
        connection: Connection = Connection(socket)
        super().__init__(connection)
