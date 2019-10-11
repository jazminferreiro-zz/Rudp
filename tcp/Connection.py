import os
from tcp.TcpSocket import TcpSocket

"""Los comandos posibles tienen 2 caracteres (para no tener que recibir el largo del comando)
    las opciones son:
    ok = para empezar a enviar el mensaje
    dl = download
    ul = upload
    sd = shutdown connection
    se envia el largo del archivo terminado en punto por ejemplo "100."
"""


class ConnectionProtocol(object):
    CHUNK_SIZE = 1024
    CODE_LEN = 2
    OK = "ok"
    DOWNLOAD = "dl"
    UPLOAD = "ul"

    def __innit__(self, storage_dir: str, conn_socket: TcpSocket):
        self.storage_dir = storage_dir
        self.conn_socket = conn_socket

    # envio y recibo codigos de 2 bytes

    def send_code(self, code: str):
        self.conn_socket.send_bytes(code.encode())

    def recv_code(self)-> str:
        return self.conn_socket.receive_bytes(self.CODE_LEN).decode()

    def wait_ok_signal(self):
        signal = self.recv_code().decode()
        if signal != self.OK:
            print("There was an error in connection, ok never received")
            return exit(1)

    # envio y recibo numeros

    def send_number(self, num: int):
        self.conn_socket.send_bytes(str(int).encode())

    def recv_number(self) -> int:
        data = self.conn_socket.receive_bytes(self.CHUNK_SIZE)
        return int(data)

    # envio y recibo nombres de archivos

    def recv_filename(self):
        # Recepción file_name length
        filename_size = self.recv_number()
        print('filename length: {}'.format(filename_size))

        # Envío OK
        self.send_code(self.OK)

        # Recepción nombre de archivo
        filename = self.conn_socket.receive_bytes(filename_size)
        filename = "{}/{}".format(self.storage_dir, filename)
        print('filename: {}'.format(filename))
        return filename

    def send_filename(self, name):
        # Envío largo nombre de archivo
        name = name.encode()
        filename_size = len(name)
        self.send_number(filename_size)

        # Espero OK de svr
        self.wait_ok_signal()

        # Envío nombre de archivo al servidor
        self.conn_socket.send_bytes(name)

    # envio y recibo archivos

    def recv_file(self, filename):
        # Recepción cantidad de bytes de archivo
        file_size = self.recv_number()
        self.send_code(self.OK)

        f = open(filename, "wb")

        bytes_recv = 0
        while bytes_recv < file_size:
            data = self.conn_socket.receive_bytes(self.CHUNK_SIZE)
            bytes_recv += len(data)
            f.write(data)
        f.close()
        print("Received file {}".format(filename))

    def send_file(self, filename):
        # Envío de archivo
        f = open(filename, "rb")
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0, os.SEEK_SET)

        print("Sending {} bytes from {}".format(file_size, filename))

        # Envío tamaño de archivo en bytes
        self.send_number(file_size)
        self.wait_ok_signal()

        bytes_sent = 0
        while bytes_sent < file_size:
            chunk = f.read(self.CHUNK_SIZE)
            if not chunk:
                break
            bytes_sent += self.conn_socket.send_bytes(chunk)

        # Cierro archivo
        f.close()
