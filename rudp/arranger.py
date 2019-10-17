from rudp.actor import Actor

class Arranger(Actor):
    def __init__(self, recv_queue):
        super().__init__()
        self.recv_queue = recv_queue
        self.exp_seq = 0
        self.packs = []
        self.seq_num_received = set()

    def run(self):
        while True:
            pack = self.get()
            if pack is None:
                self.task_done()
                break
            self.arrange(pack)

    def arrange(self, pack):
        seq_num = pack.get('header').get('seq_num')

        if seq_num in self.seq_num_received:
            self.task_done()
            return # drop duplicated packs with payload

        self.seq_num_received.add(seq_num)
        self.packs.append((seq_num, pack))
        self.packs.sort()
        self.release_sequential_pack()

    def release_sequential_pack(self):
        while len(self.packs) > 0:
            min_seq_num, min_pack = min(self.packs)
            if min_seq_num == self.exp_seq:
                self.packs.remove((min_seq_num, min_pack))
                self.recv_queue.put(min_pack)
                self.exp_seq += 1
                self.task_done()
            else:
                return
