from rudp.actor import Actor
import heapq

class Handler(Actor):
    def __init__(self, recv_queue):
        super().__init__()
        self.data_collection = []
        self.seq_num_record = set()
        self.recv_queue = recv_queue
        self.expected_seq_num = 0

    def run(self):
        while True:
            data = self.get()
            if data is None:
                self.task_done()
                break

            seq_num = data.get('header').get('seq_num')

            if seq_num not in self.seq_num_record:
                self.data_collection.append((seq_num, data))
                self.seq_num_record.add(seq_num)
                self.put_sequantial_data()
            self.task_done()


    def put_sequantial_data(self):
        self.data_collection.sort()
        while len(self.data_collection) > 0:
            smallest_seq_num, data = self.data_collection.pop(0)
            if self.expected_seq_num == smallest_seq_num:
                self.expected_seq_num += 1
                self.recv_queue.put(data)
            else:
                self.data_collection.insert(0, (smallest_seq_num, data))
                return
