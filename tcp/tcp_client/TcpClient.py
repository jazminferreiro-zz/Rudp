import os

from tcp.Connection import Connection
from tcp.TcpSocket import TcpSocket


class TcpClient():
    def __init__(self, server_address):
        socket = TcpSocket(server_address)
        socket.connect()
        self.connection = Connection(socket)

    def download(self, filename, destination):
        self.connection.send_code(self.connection.DOWNLOAD)
        self.connection.wait_ok_signal()
        self.connection.send_filename(filename)
        self.connection.wait_ok_signal()
        self.connection.recv_file(destination)


    def upload(self, filename, source):
        self.connection.send_code(self.connection.UPLOAD)
        self.connection.wait_ok_signal()
        self.connection.send_filename(filename)
        self.connection.wait_ok_signal()
        self.connection.send_file(source)

