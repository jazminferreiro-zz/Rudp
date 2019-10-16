from rudp.thread import Thread
import socket
import pickle

class Receiver(Thread):
    BUFSIZE = 1024

    def __init__(self, recv_sock, sender):
        super().__init__()
        self.recv_sock = recv_sock
        self.sender = sender

    def run(self):
        print('-- init receiver')
        while True:
            data, addr = self.recv_sock.recvfrom(self.BUFSIZE)
            if addr is None:
                print('-- receiver breaking while')
                break
            data = pickle.loads(data)
            print('-- receiver receiving data {} from addr {}'.format(data, addr))

            if data.get('payload'):
                ack_pack = {
                    'header': {
                        'is_ack': True,
                        'ack_num': data.get('header').get('seq_num'),
                        'dst_recv_addr': data.get('header').get('src_recv_addr')
                    }
                }
                self.sender.put(ack_pack)
                print('-- receiver -- ack_pack --> sender,  ', ack_pack)
        print('-- end receiver')

    def stop(self):
        try:
            pass
            self.recv_sock.shutdown(socket.SHUT_RD)
        except:
            print('-- receiver recv_sock.shutdown()')
