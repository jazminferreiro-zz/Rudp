import socket
import pickle

class RudpSocket(object):
    TIMEOUT = 1
    BUFSIZE = 1024

    def __init__(self):
        self.seq_num = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendto(self, payload, addr):
        keep_resending = True
        self.seq_num += 1

        # seq_num como string para que sea visible en wireshark
        package = {
            'header': {'seq_num': str(self.seq_num)},
            'payload': payload
        }
        bytes_package = pickle.dumps(package)

        while keep_resending:
            bytes_sent = self.sock.sendto(bytes_package, addr)
            # self.sock.settimeout(self.TIMEOUT)
            try:
                ack_data, addr = self.sock.recvfrom(self.BUFSIZE)
                ack_package = pickle.loads(ack_data)
                ack = ack_package.get('header').get('ack')
                if ack == str(self.seq_num):
                    keep_resending = False
            except:
                pass

    def recvfrom(self, bufsize):
        data, addr = self.sock.recvfrom(bufsize)
        if not data:
            return data, addr
        else:
            package = pickle.loads(data)
            ack_package = {'header': {'ack': package.get('header').get('seq_num')}}
            self.sock.sendto(pickle.dumps(ack_package), addr)
            return package.get('payload'), addr

    def bind(self, addr):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)

    def shutdown(self, flag):
        self.sock.shutdown(flag)

    def close(self):
        self.sock.close()