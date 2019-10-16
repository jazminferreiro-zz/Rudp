from rudp.rudp_socket import RudpSocket
import time

CLI_RECV_ADDR = ('127.0.0.1', 5001)
SV_SEND_ADDR = ('127.0.0.1', 9000)
BUFSIZE = 1024

def main():
    print('init server')

    rudp = RudpSocket(SV_SEND_ADDR)
    data, addr = rudp.recvfrom(BUFSIZE)

    time.sleep(10)
    rudp.close()

    print('end server')

main()
