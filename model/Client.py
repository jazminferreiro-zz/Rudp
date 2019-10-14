import threading

from model.Connection import Connection



class Client():
    def __init__(self, connection: Connection):
        self.connection = connection
        self.principal_thread = None

    def download(self, filename, destination):
        self.principal_thread = threading.Thread(name="download",target=self.run_download, args= (filename, destination,))
        self.principal_thread.start()

    def run_download(self, filename, destination):
        try:
            self.connection.send_code(self.connection.DOWNLOAD)
            self.connection.send_filename(filename)
            self.connection.recv_file(destination)
        except OSError:
            pass  # cerrearon el socket udc

    def upload(self, filename, destination):
        self.principal_thread = threading.Thread(name="upload",target=self.run_upload, args= (filename, destination,))
        self.principal_thread.start()



    def run_upload(self, filename, source):
        try:
            self.connection.send_code(self.connection.UPLOAD)
            self.connection.send_filename(filename)
            self.connection.send_file(source)
        except OSError:
            pass  # cerrearon el socket udp

    def stop_running(self):
        self.connection.close()
        if(self.principal_thread != None):
            self.principal_thread.join(timeout=1)
            self.principal_thread.join()