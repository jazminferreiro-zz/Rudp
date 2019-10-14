import random
import socket
import pickle
from datetime import datetime

from model.Socket import Socket

"""
Socket UDP
envia y recibe bytes
"""


class UdpSocket(Socket):
    TIMEOUT = 10  # segundos

    def __init__(self, own_address: tuple):
        # Creación socket UDP
        self.own_address = own_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setblocking(False)  # no blockeante
        self.sock.settimeout(self.TIMEOUT)
        self.is_connected = False
        self.conn_adress = None
        self.seq_num = 0 #random.randint(0, 100)
        self.seq_recd = [] #guardo los seq_number de paquetes recibidos para descartar duplicados

    def bind_and_listen(self):
        # Bind socket a host:port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.own_address)
        self.connect()


    def connect(self, conn_addr = None ):
        self.is_connected = True
        self.conn_adress = conn_addr
        self.seq_recd = []
        #si es el servidor no sabra cual es la direccion del cliente hasta no recibir unmensaje


    def stop(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.is_connected = False


    """
      voy mandando un paquete por vez.
      si no recibo el ack despues del timestamp lo reenvio
      """
    def send_bytes(self, msg: bytes) -> int:
        if not self.is_connected:
            raise RuntimeError("socket not connected")
        msg_len = len(msg)
        total_ack = 0
        forwarded = 0
        while total_ack < msg_len:
            package = self.pack(msg, total_ack)
            sent = self.sock.sendto(pickle.dumps(package), self.conn_adress)
            if sent == 0:
                print("Error sending msg")
                raise RuntimeError("socket connection broken")
            elif (self.wait_ack()):
                total_ack = total_ack + len(package.get('payload'))
                self.seq_num = self.seq_num + sent #nuevo paquete, sino reenvio el mismo
            else:
                forwarded += 1
                if(forwarded == 3):
                    self.seq_num = self.seq_num + sent
                    break #si el paquete ya se reenvio 3 veces debe haberse cerrado la conexion!
        return total_ack


    #como los paquetes son objetos se deben serializar y deserializar
    #para eso necesitan tener un tamaño fino = MSS
    #un paquete con payload vacio ocupa 70
    def pack(self, msg: bytes, total_ack: bytes):
        package = {
            'header': {'seq_num': self.seq_num},
            'payload': ''
        }
        payload_las_byte = total_ack + self.MSS - len(pickle.dumps(package))
        payload = msg[total_ack:min(len(msg), payload_las_byte)]
        package['payload'] = payload
        print("----------------------> enviando paquete {} = '{}...'".format(self.seq_num, payload.decode()[0:min(10, len(payload))]))
        return package


    #Espera a recibir el ack del seq num recien enviado
    #si no lo recibe pasado el timeout lo tomara como perdido
    def wait_ack(self) -> bool:
        try:
            ack_data, addr = self.sock.recvfrom(self.MSS)
        except socket.timeout:
            return False
        if (self.conn_adress != None and  self.conn_adress != addr):
            print("No es posible atender mas de una conexion cliente-servidor por vez")
        ack_package = pickle.loads(ack_data)
        ack_num = ack_package.get('header').get('ack')
        if (ack_num == self.seq_num + 1):
            print("------------------ paquete {} recibido correctamente".format(self.seq_num))
            return True
        return False



    def receive_bytes(self, size: int) -> bytes:
        if not self.is_connected:
            raise RuntimeError("socket not connected")
        chunks = []
        bytes_recd = 0
        while bytes_recd < size:
            try:
                data, addr= self.sock.recvfrom(self.MSS)
            except:
                print("esperando paquetes para completar mensaje......")
                continue #sigo esperando recibir data
            if (self.conn_adress == None):
                self.conn_adress = addr
            elif(self.conn_adress != addr):
                print("No es posible atender mas de una conexion cliente-servidor por vez")
                continue
            if data == '':
                print("Error receiving msg")
                raise RuntimeError("socket connection broken")
            package = pickle.loads(data)
            self.send_ack(package)
            seq_num_received = package.get('header').get('seq_num')
            if(seq_num_received in self.seq_recd):
                print("paquete duplicado")
                continue #paquete duplicado, lo descarto
            self.seq_recd.append(seq_num_received)
            payload = package.get('payload')
            chunks.append(payload)
            bytes_recd = bytes_recd + len(payload)
        return b''.join(chunks)


    # en el ack mando la cantidad  de bytes recibidos
    def send_ack(self, package):
        print("<---------------------- recibi paquete {} ".format( package.get('header').get('seq_num')))
        package_seq_num = package.get('header').get('seq_num') + 1
        package = {
            'header': {'ack': package_seq_num},
        }
        sent =self.sock.sendto(pickle.dumps(package), self.conn_adress)
        return sent