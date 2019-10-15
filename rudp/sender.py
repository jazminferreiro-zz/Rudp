from rudp.actor import Actor
from rudp.worker import Worker
from  concurrent.futures import ThreadPoolExecutor

class Sender(Actor):
    MAX_RUNNING_WORKERS = 1

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.seq_num = 0
        self.workers = {}

    def run(self):
        with ThreadPoolExecutor(max_workers=self.MAX_RUNNING_WORKERS) as executor:
            while True:
                msg = self.get()
                print('sender: ', msg)
                if msg is None:
                    self.task_done()
                    break

                if msg.get('header').get('is_ack'):
                    worker, handle = self.workers[msg.get('header').get('ack_num')]
                    worker.data_is_acknowledge()
                    handle.result()
                    print('-FIN WORKER-{}'.format(msg.get('header').get('ack_num')))
                else:
                    worker = self.create_worker(msg, executor)
                self.task_done()
            print('***FIN SENDER***')

    def wait_for_all_workers_to_stop(self):
        for seq_num, (worker, handle) in self.workers.items():
            handle.result()

    def create_worker(self, msg, executor):
        worker = Worker(msg, self.sock)
        msg['header']['seq_num'] = self.seq_num
        self.workers[self.seq_num] = (worker, executor.submit(worker.run))
        self.seq_num += 1
