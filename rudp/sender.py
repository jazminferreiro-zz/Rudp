from rudp.actor import Actor
import pickle

class Sender(Actor):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            pack = self.get()

            if pack is None:
                self.task_done()
                break
                
            self.sock.sendto(
                pickle.dumps(pack),
                pack.get('header').get('dst_addr')
            )
            self.task_done()
