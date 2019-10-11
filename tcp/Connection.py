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


class Connection:
    CHUNK_SIZE = 1024
    NUM_LEN = 10
    CODE_LEN = 2

    OK = "ok"
    DOWNLOAD = "dl"
    UPLOAD = "ul"

    def __init__(self, socket: TcpSocket):
        self.socket = socket
        if not (self.socket.is_connected):
            raise RuntimeError("Connection is broken")

    # envio y recibo codigos de 2 bytes para los comandos
    def send_code(self, code: str):
        self.socket.send_bytes(code.encode())

    def recv_code(self)-> str:
        return self.socket.receive_bytes(self.CODE_LEN).decode()

    def wait_ok_signal(self):
        signal = self.recv_code()
        if signal != self.OK:
            print("There was an error in connection, ok never received")
            return exit(1)

    # envio y recibo numeros

    def send_number(self, num: int):
        nun_in_ten_bytes = '{:>10}'.format(str(num)).encode()
        self.socket.send_bytes(nun_in_ten_bytes)

    def recv_number(self) -> int:
        data = self.socket.receive_bytes(self.NUM_LEN)
        return int(data)

    # envio y recibo nombres de archivos

    def recv_filename(self)-> str:
        # Recepción file_name length
        filename_size = self.recv_number()
        print('filename length: {}'.format(filename_size))

        # Envío OK
        self.send_code(self.OK)

        # Recepción nombre de archivo
        filename = self.socket.receive_bytes(filename_size)
        return filename.decode()

    def send_filename(self, name: str):
        # Envío largo nombre de archivo
        name = name.encode()
        filename_size = len(name)
        self.send_number(filename_size)

        # Espero OK de svr
        self.wait_ok_signal()

        # Envío nombre de archivo al servidor
        self.socket.send_bytes(name)

    # envio y recibo archivos

    def recv_file(self, filename_path):
        # Recepción cantidad de bytes de archivo
        file_size = self.recv_number()
        self.send_code(self.OK)

        f = open(filename_path, "wb")

        bytes_recv = 0
        while bytes_recv < file_size:
            data = self.socket.receive_bytes(min(self.CHUNK_SIZE, file_size - bytes_recv))
            bytes_recv += len(data)
            f.write(data)
        f.close()
        print("Received file {}".format(filename_path))

    def send_file(self, filename_path):
        # Envío de archivo
        f = open(filename_path, "rb")
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0, os.SEEK_SET)

        print("Sending {} bytes from {}".format(file_size, filename_path))

        # Envío tamaño de archivo en bytes
        self.send_number(file_size)
        self.wait_ok_signal()

        bytes_sent = 0
        while bytes_sent < file_size:
            chunk = f.read(min(self.CHUNK_SIZE, file_size - bytes_sent))
            if not chunk:
                break
            bytes_sent += self.socket.send_bytes(chunk)

        # Cierro archivo
        f.close()
