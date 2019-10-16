from rudp.actor import Actor

class Arranger(Actor):
    def __init__(self):
        super().__init__()

    def run(self):
        print('-- init arranger')
        while True:
            pack = self.get()
            if pack is None:
                self.task_done()
                break
            print('-- arrenger got pack: ', pack)
            self.task_done()
        print('-- end arranger')
