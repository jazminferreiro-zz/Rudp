from rudp.actor import Actor
import pickle

class Sender(Actor):
    def __init__(self, send_sock):
        super().__init__()
        self.send_sock = send_sock

    def run(self):
        print('-- init sender')
        while True:
            data = self.get()
            if data is None:
                self.task_done()
                break
            print('-- sender sending data', data)
            self.send_sock.sendto(
                pickle.dumps(data),
                data.get('header').get('dst_recv_addr')
            )
            self.task_done()
        print('-- sender qsize() = ', self.queue.qsize())
        print('-- end sender')

    # TODO: delete
    def stop(self):
        self.queue.put(None)
        print('-- sender put None')
        self.queue.join()
        print('-- sender queue joined')
        self.thread.join()
        print('-- sender thread joined')
