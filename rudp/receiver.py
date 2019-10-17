from rudp.thread import Thread
import socket
import pickle

class Receiver(Thread):
    BUFSIZE = 1024

    def __init__(self, recv_sock, sender, scheduler, arranger):
        super().__init__()
        self.recv_sock = recv_sock
        self.sender = sender
        self.scheduler = scheduler
        self.arranger = arranger

    def run(self):
        while True:
            data, addr = self.recv_sock.recvfrom(self.BUFSIZE)
            if addr is None:
                break
            pack = pickle.loads(data)

            if pack.get('payload'):
                self.arranger.put(pack)
                self.send_back_ack(pack)
            elif pack.get('header').get('is_ack'):
                self.acknowledge_pack(pack)

    def stop(self):
        try:
            self.recv_sock.shutdown(socket.SHUT_RD)
        except:
            pass

    def send_back_ack(self, pack):
        ack_pack = {
            'header': {
                'is_ack': True,
                'ack_num': pack.get('header').get('seq_num'),
                'dst_recv_addr': pack.get('header').get('src_recv_addr')
            }
        }
        self.sender.put(ack_pack)

    def acknowledge_pack(self, pack):
        self.scheduler.put(pack)
