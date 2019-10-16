from rudp.actor import Actor

class Arranger(Actor):
    def __init__(self, recv_queue):
        super().__init__()
        self.recv_queue = recv_queue

    def run(self):
        print('-- init arranger')
        while True:
            pack = self.get()
            if pack is None:
                self.task_done()
                break
            print('-- arrenger got pack: ', pack)
            print('-- arranger sending --> rudp')
            self.recv_queue.put(pack)
            self.task_done()
        print('-- end arranger')
