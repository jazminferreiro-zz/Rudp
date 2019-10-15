from rudp.thread import Thread
import socket
import pickle
import time

class Receiver(Thread):
    BUFSIZE = 1024

    def __init__(self, sock, handler, sender):
        super().__init__()
        self.sock = sock
        self.sender = sender
        self.handler = handler

    def run(self):
        print('Im receiver')
        while True:
            data, addr = self.sock.recvfrom(self.BUFSIZE)
            if addr is None:
                break

            loaded_data = pickle.loads(data)
            print('receiver, data:', loaded_data, ' addr: ', addr)


            if  loaded_data.get('header').get('is_ack'):
                self.sender.put(loaded_data)
            else:
                next_msg = {
                    'header': {
                        'is_ack': True,
                        'ack_num': loaded_data.get('header')['seq_num']
                    }
                }
                print('receiver sending ack: ', next_msg, ' addr: ', addr)
                self.sock.sendto(pickle.dumps(next_msg), addr)
                self.handler.put(loaded_data)
        print('FIN RECEIVER')

    def stop(self):
        try:
            self.sock.shutdown(socket.SHUT_RD)
        except:
            pass
