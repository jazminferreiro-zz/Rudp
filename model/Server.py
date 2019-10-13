from model.Connection import Connection

import os


class Server(object):
    def __init__(self,  storage_dir):
        self.storage_dir = storage_dir
        self.create_dir()

    def reset(self):
        #para resetear la conexion UDP
        pass

    def new_connection(self, connection: Connection):
        self.connection = connection

    def create_dir(self):
        """ Validación de directorio, si no existe lo crea. """
        if not os.path.exists(self.storage_dir):
            os.mkdir(self.storage_dir)
            print('Dir: {} created!'.format(self.storage_dir))

    def execute_command(self):
        self.reset()
        print("listo para aceptar nuevas conexiones")
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
            print("comando invalido")
            return False

    def get_filename_path(self):
        filename = self.connection.recv_filename()
        filename_path = "{}/{}".format(self.storage_dir, filename)
        print('filename: {}'.format(filename_path))
        return filename_path