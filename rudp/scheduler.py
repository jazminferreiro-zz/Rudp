from rudp.actor import Actor
from rudp.worker import Worker
from  concurrent.futures import ThreadPoolExecutor

class Scheduler(Actor):
    MAX_WORKERS = 1

    def __init__(self, send_sock):
        super().__init__()
        self.seq_num = 0
        self.workers = {}
        self.send_sock = send_sock

    def run(self):
        print('init scheduler')
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            while True:
                pack = self.get()
                if pack is None:
                    self.task_done()
                    break
                self.submit_worker(executor, pack)
                self.task_done()
        print('end scheduler')

    def submit_worker(self, executor, pack):
        pack['header']['seq_num'] = self.seq_num
        worker = Worker(pack, self.send_sock)
        handler = executor.submit(worker.run)
        self.workers[self.seq_num] = (worker, handler)
        handler.result()
