from rudp.rudp_socket import RudpSocket
import time

CLI_RECV_ADDR = ('127.0.0.1', 5001)
SV_SEND_ADDR = ('127.0.0.1', 9000)
BUFSIZE = 1024
IS_CLIENT = False


def main():
    print('init server')

    rudp = RudpSocket(SV_SEND_ADDR)
    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto(b'ok_start', addr)

    for i in range(10):
        data, addr = rudp.recvfrom(BUFSIZE)
        rudp.sendto('arrived msg {}'.format(i), addr)
        print(data)

    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.sendto(b'ok_fin', addr)

    time.sleep(10)
    rudp.close()

    print('end server')

main()
