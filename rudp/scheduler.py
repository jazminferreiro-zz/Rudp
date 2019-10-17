from rudp.actor import Actor
from rudp.worker import Worker
from rudp.sender import Sender
from  concurrent.futures import ThreadPoolExecutor
import pdb
import os
import __main__

class Scheduler(Actor):
    MAX_WORKERS = 10

    def __init__(self, sender):
        super().__init__()
        self.seq_num = 0
        self.workers = {}
        self.sender = sender

    def run(self):
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            while True:
                pack = self.get()

                if pack is None:
                    self.task_done()
                    break

                if pack.get('payload'):
                    self.submit_worker(executor, pack)
                elif pack.get('header').get('is_ack'):
                    self.stop_worker_if_exists(pack)
                    self.task_done()

    def submit_worker(self, executor, pack):
        pack['header']['seq_num'] = self.seq_num
        worker = Worker(pack, self.sender)
        handler = executor.submit(worker.run)
        self.workers[self.seq_num] = (worker, handler)
        self.seq_num += 1

    def stop_worker_if_exists(self, pack):
        ack_num = pack.get('header').get('ack_num')
        if self.workers.get(ack_num):
            worker, handler = self.workers.get(ack_num)
            worker.stop()
            handler.result()
            self.workers.pop(ack_num)
            self.task_done()
