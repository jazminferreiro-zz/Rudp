from rudp.rudp_socket import RudpSocket
import time

CLI_ADDR = ('127.0.0.1', 5000)
SV_ADDR = ('127.0.0.1', 9000)

BUFSIZE = 1024
IS_CLIENT = False
OUTPUT_DIR = './output'
FILEBUFSIZE = int(BUFSIZE / 2)

def main():
    print('init server')
    rudp = RudpSocket(SV_ADDR)

    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('start_ok', addr)

    name, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('name_ok', addr)

    print('-!!!!!!!!! NAME: {}!!!!!!!'.format(name))

    size, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('size_ok', addr)

    print('-!!!!!!!!! SIZE: {}!!!!!!!'.format(size))

    with open('{}/{}'.format(OUTPUT_DIR, name), 'wb') as file:
        bytes_read = 0
        while bytes_read < size:
            chunk, addr = rudp.recvfrom(FILEBUFSIZE)
            bytes_read += len(chunk)
            file.write(chunk)

    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('fin_ok', addr)

    print('zzzzzzzzzzzzzzzzz  server enters sleep')
    rudp.wait_last_ack()
    rudp.close()

    print('end server')

main()
