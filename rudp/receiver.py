from rudp.thread import Thread
import socket

class Receiver(Thread):
    BUFSIZE = 1024

    def __init__(self, recv_sock):
        super().__init__()
        self.recv_sock = recv_sock

    def run(self):
        print('-- init receiver')
        while True:
            data, addr = self.recv_sock.recvfrom(self.BUFSIZE)
            if addr is None:
                print('-- receiver breaking while')
                break
            print('-- receiver receiving data {} from addr {}'.format(data, addr))
        print('-- end receiver')

    def stop(self):
        try:
            pass
            self.recv_sock.shutdown(socket.SHUT_RD)
        except:
            print('-- receiver recv_sock.shutdown()')
