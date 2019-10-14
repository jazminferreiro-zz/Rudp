import socket

"""
Socket Abstracto
Solo para definir los metodos que tiene 
"""
class Socket(object):
    MSS = 1024
    NUM_SIZE = 10
    FIN = "FIN"
    def bind_and_listen(self) :
        pass
    def accept(self):
        pass

    def connect(self):
        pass

    def stop(self):
        pass

    def send_bytes(self, msg: bytes)-> int:
        pass


    def receive_bytes(self, size: int)-> bytes:
        pass