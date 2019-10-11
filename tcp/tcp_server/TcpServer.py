from tcp.Connection import Connection
from tcp.TcpSocket import TcpSocket
import os


class TcpServer:
    def __init__(self, server_address, storage_dir):
        self.storage_dir = storage_dir
        self.create_dir()
        self.server_socket = TcpSocket(server_address)
        self.server_socket.bind_and_listen()
        self.connect_with_client()


    def connect_with_client(self):
        socket = self.server_socket.accept()
        self.connection = Connection( socket)

    def create_dir(self):
        """ Validación de directorio, si no existe lo crea. """
        if not os.path.exists(self.storage_dir):
            os.mkdir(self.storage_dir)
            print('Dir: {} created!'.format(self.storage_dir))

    def execute_command(self):
        command = self.connection.recv_code()
        if command == self.connection.DOWNLOAD:
            print("EL cliente solicita descargar archivo")
            self.connection.send_file(self.get_filename_path())
            return True
        elif command == self.connection.UPLOAD:
            print("El cliente solicito subir archivo")
            self.connection.recv_file(self.get_filename_path())
            return True
        else:
            return False

    def get_filename_path(self):
        filename = self.connection.recv_filename()
        filename_path = "{}/{}".format(self.storage_dir, filename)
        print('filename: {}'.format(filename_path))
        return filename_path