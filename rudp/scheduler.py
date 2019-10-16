from rudp.actor import Actor

class Scheduler(Actor):
    def __init__(self):
        super().__init__()
        self.seq_num = 0

    def run(self):
        print('init scheduler')
        while True:
            data = self.get()
            if data is None:
                self.task_done()
                break
            print(data)
            self.task_done()
        print('end scheduler')
