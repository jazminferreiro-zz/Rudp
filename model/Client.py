from model.Connection import Connection
from model.tcp.TcpSocket import TcpSocket


class Client():
    def __init__(self, connection: Connection):
        self.connection = connection

    def download(self, filename, destination):
        self.connection.send_code(self.connection.DOWNLOAD)
        self.connection.send_filename(filename)
        self.connection.recv_file(destination)

    def upload(self, filename, source):
        self.connection.send_code(self.connection.UPLOAD)
        self.connection.send_filename(filename)
        self.connection.send_file(source)