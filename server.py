from rudp.rudp_socket import RudpSocket
import time

CLI_RECV_ADDR = ('127.0.0.1', 5001)
SV_SEND_ADDR = ('127.0.0.1', 9000)
BUFSIZE = 1024
IS_CLIENT = False
OUTPUT_DIR = './output'
FILEBUFSIZE = int(BUFSIZE / 2)

def main():
    print('init server')
    rudp = RudpSocket(SV_SEND_ADDR)

    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('start_ok', addr)

    name, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('ok', addr)

    print('-!!!!!!!!! NAME: {}!!!!!!!'.format(name))

    size, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('ok', addr)

    print('-!!!!!!!!! SIZE: {}!!!!!!!'.format(size))

    with open('{}/{}'.format(OUTPUT_DIR, name), 'wb') as file:
        bytes_read = 0
        while bytes_read < size:
            chunk, addr = rudp.recvfrom(FILEBUFSIZE)
            bytes_read += len(chunk)
            file.write(chunk)

    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto('fin_ok', addr)

    time.sleep(5)
    rudp.close()

    print('end server')

main()
