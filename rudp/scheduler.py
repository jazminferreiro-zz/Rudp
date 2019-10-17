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
                    self.stop_worker_if_exists(pack)
                    self.task_done()

        print('-- scheduler qsize() = ', self.queue.qsize())
        print('-- end scheduler')

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

    # TODO: delete
    def stop(self):
        self.queue.put(None)
        print('-- scheduler put None')
        self.queue.join()
        print('-- scheduler queue joined')
        self.thread.join()
        print('-- scheduler thread joined')
