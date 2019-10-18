from udp.connection import Connection

class UdpClient(object):
    OWN_ADDR = ('127.0.0.1', 5000)

    def upload(self, server_address, src, name):
        connection = Connection(self.OWN_ADDR)
        connection.sendto('upload', server_address)
        connection.sendto(name, server_address)
        connection.send_file(src, server_address)
        connection.close()


    def download(self, server_address, name, dest):
        connection = Connection(self.OWN_ADDR)
        connection.sendto('download', server_address)
        connection.sendto(name, server_address)
        connection.recv_file(dest)
        connection.close()
