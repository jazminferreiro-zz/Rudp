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
        print('-- init scheduler')

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            while True:
                pack = self.get()
                print('-- scheduler got pack :', pack)

                if pack is None:
                    self.task_done()
                    break

                if pack.get('payload'):
                    print('--scheduler submitting worker , pack: ', pack)
                    self.submit_worker(executor, pack)
                elif pack.get('header').get('is_ack'):
                    print('-- scheduler stopping worker, pack', pack)
                    self.stop_worker(pack)
                    self.task_done()
                    self.task_done()

        print('-- end scheduler')

    def submit_worker(self, executor, pack):
        pack['header']['seq_num'] = self.seq_num
        worker = Worker(pack, self.sender)
        handler = executor.submit(worker.run)
        self.workers[self.seq_num] = (worker, handler)

    def stop_worker(self, pack):
        worker, handler = self.workers.get(pack.get('header').get('ack_num'))
        worker.stop()
        handler.result()
