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
        print('-- init receiver')
        while True:
            data, addr = self.recv_sock.recvfrom(self.BUFSIZE)
            if addr is None:
                print('-- receiver breaking while')
                break
            pack = pickle.loads(data)
            print('-- receiver receiving pack {} from addr {}'.format(pack, addr))

            if pack.get('payload'):
                self.arranger.put(pack)
                self.send_back_ack(pack)
            elif pack.get('header').get('is_ack'):
                self.acknowledge_pack(pack)

        print('-- end receiver')

    def stop(self):
        try:
            pass
            self.recv_sock.shutdown(socket.SHUT_RD)
        except:
            print('-- receiver recv_sock.shutdown()')

    def send_back_ack(self, pack):
        ack_pack = {
            'header': {
                'is_ack': True,
                'ack_num': pack.get('header').get('seq_num'),
                'dst_recv_addr': pack.get('header').get('src_recv_addr')
            }
        }
        print('-- receiver -- ack_pack --> sender,  ', ack_pack)
        self.sender.put(ack_pack)

    def acknowledge_pack(self, pack):
        print('-- receiver -- ack --> scheduler,  ', pack)
        self.scheduler.put(pack)
