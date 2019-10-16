class Worker(object):
    def __init__(self, pack, send_sock):
        self.pack = pack
        self.send_sock = send_sock

    def run(self):
        print('init worker')
        print('worker: ', self.pack)
        print('worker sending package')
        print('end worker')
