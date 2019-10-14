import threading

from model.Connection import Connection

import os


class Server(object):
    def __init__(self,  storage_dir):
        self.storage_dir = storage_dir
        self.create_dir()
        self.principal_thread = threading.Thread(name="server-listen",target=self.listen)
        self.continue_listening = False

    def new_connection(self, connection: Connection):
        self.connection = connection

    def stop_running(self, connection: Connection = None):
        self.continue_listening = False
        connection.close()
        if(connection != None):
            connection.close()
        self.principal_thread.join(timeout=1)
        self.principal_thread.join()

    def start_listenning(self):
        self.continue_listening = True
        self.principal_thread.start()


    def listen(self):
        while(self.continue_listening):
            self.connect_with_client()
            self.execute_command()
            self.reset()
            print("listo para aceptar nuevas conexiones")
            #except(OSError,AttributeError):
                #print(" se cerro el server")



    def connect_with_client(self):
        #para que ejecute methodo diferente dependiendo de si es udp o tpc
        pass

    def reset(self):
        #para resetear la conexion UDP
        pass


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
            print("comando invalido")
            return False

    def get_filename_path(self):
        filename = self.connection.recv_filename()
        filename_path = "{}/{}".format(self.storage_dir, filename)
        print('filename: {}'.format(filename_path))
        return filename_path