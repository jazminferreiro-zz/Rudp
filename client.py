from rudp.rudp_socket import RudpSocket
import time
import os

CLI_ADDR = ('127.0.0.1', 5000)
SV_ADDR = ('127.0.0.1', 9000)
BUFSIZE = 1024
FILEBUFSIZE = int(BUFSIZE)

NAME = 'example2.txt'
SRC = './files/{}'.format(NAME)


def file_size(f):
     f.seek(0, os.SEEK_END)
     size = f.tell()
     f.seek(0, os.SEEK_SET)
     return size

def main():
    print('init client')
    rudp = RudpSocket(CLI_ADDR)

    # init connection
    rudp.sendto('start', SV_ADDR)
    data, addr = rudp.recvfrom(BUFSIZE)
    if data != 'start_ok':
        print('start error')
        rudp.close()
        return

    rudp.sendto(NAME, SV_ADDR)
    rudp.recvfrom(BUFSIZE)

    with open(SRC, 'rb') as file:
        rudp.sendto(file_size(file), SV_ADDR)
        rudp.recvfrom(BUFSIZE)

        while True:
            chunk = file.read(FILEBUFSIZE)
            if not chunk:
                break
            rudp.sendto(chunk, SV_ADDR)

    # end connecetion
    rudp.sendto('fin', SV_ADDR)
    data, addr = rudp.recvfrom(BUFSIZE)
    if data != 'fin_ok':
        print('fin error')
        rudp.close()
        return

    print('zzzzzzzzzzzzzzzzzz client enters sleep')
    rudp.close()

    print('end client')

main()
