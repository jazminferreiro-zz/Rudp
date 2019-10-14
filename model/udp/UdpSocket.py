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
    FINISH_TRY = 5 # intentos para enviar el fin
    END = 'end'
    ACK = 'ack'
    HEADER = 'header'
    PAYLOAD = 'payload'
    SEQ_NUM = 'seq_num'
    

    def __init__(self, own_address: tuple):
        # Creación socket UDP
        self.own_address = own_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setblocking(False)  # no blockeante
        self.sock.settimeout(self.TIMEOUT)
        self.is_connected = False
        self.conn_adress = None
        self.seq_num = 0 #random.randint(0, 100)
        self.ack_seq_nums_list = [] #guardo los seq_number de paquetes recibidos para descartar duplicados

    def bind_and_listen(self):
        # Bind socket a host:port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.own_address)
        self.connect()


    def connect(self, conn_addr = None ):
        self.is_connected = True
        self.conn_adress = conn_addr
        self.ack_seq_nums_list = []
        #si es el servidor no sabra cual es la direccion del cliente hasta no recibir unmensaje


    def stop(self):
        try:
            print("shutdown udp socket")
            self.sock.sendto(b'shutdown', self.own_address)
            self.sock.close()
        except:
            pass
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
        while total_ack < msg_len:
            package = self.pack(msg, total_ack, False)
            sent = self.sock.sendto(pickle.dumps(package), self.conn_adress)
            if sent == 0:
                print("Error sending msg")
                raise RuntimeError("socket connection broken")
            elif (self.wait_ack()):
                total_ack = total_ack + len(package.get(self.PAYLOAD))
                self.seq_num = self.seq_num + sent #nuevo paquete, sino reenvio el mismo

        sent = self.send_fin()
        for x in range(self.FINISH_TRY):
            if(self.wait_ack()):
                break
            sent = self.send_fin()
        #despues de FINISH_TRY considero que se perdio el ack del fin
        self.seq_num = self.seq_num + sent
        return total_ack

    def send_fin(self):
        package = self.pack(b'', 0, True)
        sent = self.sock.sendto(pickle.dumps(package), self.conn_adress)
        return sent





    #como los paquetes son objetos se deben serializar y deserializar
    #para eso necesitan tener un tamaño fino = MSS
    def pack(self, msg: bytes, total_ack: int, end:bool):
        package = {
            self.HEADER: {self.SEQ_NUM: self.seq_num, self.END: end},
            self.PAYLOAD: ''.encode()
        }
        payload_last_byte = total_ack + self.MSS - len(pickle.dumps(package))
        payload = msg[total_ack:min(len(msg), payload_last_byte)]
        package[self.PAYLOAD] = payload
        while(len(pickle.dumps(package)) > self.MSS):
            payload_last_byte = payload_last_byte - 1  # pesto bytes por si se agranda un poco el picke dumps
            payload = msg[total_ack:min(len(msg), payload_last_byte)]
            package[self.PAYLOAD] = payload
        log_msg = payload.decode()[0: min(3, len(payload.decode()))]
        if(end):
            log_msg = 'END'
        print("----------------------> enviando paquete {} = '{}...'".format(self.seq_num, log_msg))
        return package


    #Espera a recibir el ack del seq num recien enviado
    #si no lo recibe pasado el timeout lo tomara como perdido
    def wait_ack(self) -> bool:
        try:
            ack_data= self.recv()
        except socket.timeout:
            return False
        ack_package = pickle.loads(ack_data)
        ack_num = ack_package.get(self.HEADER).get(self.ACK)
        if(ack_num == None):
            return False #recibio un mensaje que no es un ack
        if (ack_num > self.seq_num):
            print("------------------ paquete {} recibido correctamente".format(ack_num - 1))
            return True
        return False



    def receive_bytes(self, size: int) -> bytes:
        if not self.is_connected:
            raise RuntimeError("socket not connected")
        chunks = []
        bytes_recd = 0
        while bytes_recd < size:
            try:
               data = self.recv()
            except socket.timeout:
                print("esperando paquetes para completar mensaje......")
                continue #sigo esperando recibir data
            try:
                package = pickle.loads(data)
            except pickle.UnpicklingError:
                print("datos incompletos....")
                continue #espero que se reenvie el mensaje completo
            seq_num_received = package.get(self.HEADER).get(self.SEQ_NUM)
            if(seq_num_received in self.ack_seq_nums_list or package.get(self.HEADER).get(self.END)):
                print("..............paquete duplicado")
                self.send_ack(seq_num_received) #vuelvo a mandar el ack
                continue #paquete duplicado o end, lo descarto
            self.send_ack(seq_num_received)
            payload = package.get(self.PAYLOAD)
            chunks.append(payload)
            bytes_recd = bytes_recd + len(payload)
        finish =  self.wait_fin()
        while not finish:
            print("......................esperando el end")
            if(self.wait_fin()):
                break
        return b''.join(chunks)

    def recv(self)-> bytes:

        data, addr = self.sock.recvfrom(self.MSS)

        if (self.conn_adress == None):
            self.conn_adress = addr
        elif (self.conn_adress != addr):
            raise  RuntimeError("No es posible atender mas de una conexion cliente-servidor por vez")
        if data == '':
            print("Error receiving msg")
            raise RuntimeError("socket connection broken")
        return data


    def wait_fin(self):
        try:
            fin_data = self.recv()
        except socket.timeout:
            return False
        fin_package = pickle.loads(fin_data)
        seq_num_received = fin_package.get(self.HEADER).get(self.SEQ_NUM)
        if (seq_num_received in self.ack_seq_nums_list):
            print("........................ultimo paquete duplicado")
            self.send_ack(seq_num_received)
            return False
        if(fin_package.get(self.HEADER).get(self.END)):
            self.send_ack(seq_num_received)
            print("<------------------ paquete {} END recibido correctamente".format(seq_num_received))
            return True
        print("........................paquete END perdido {}".format(fin_package.get(self.PAYLOAD)[:2]))
        return False



    # en el ack mando la cantidad  de bytes recibidos
    def send_ack(self, seq_num: int):
        self.ack_seq_nums_list.append(seq_num)
        print("<---------------------- recibi paquete {} ".format( seq_num))
        package_seq_num = seq_num + 1
        package = {
            self.HEADER: {self.ACK: package_seq_num},
        }
        sent =self.sock.sendto(pickle.dumps(package), self.conn_adress)
        return sent