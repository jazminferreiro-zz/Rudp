from rudp.actor import Actor
import pickle

class Sender(Actor):
    def __init__(self, send_sock):
        super().__init__()
        self.send_sock = send_sock

    def run(self):
        while True:
            data = self.get()
            if data is None:
                self.task_done()
                break

            self.send_sock.sendto(
                pickle.dumps(data),
                data.get('header').get('dst_recv_addr')
            )
            self.task_done()
