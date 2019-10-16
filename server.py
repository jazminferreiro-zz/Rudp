from rudp.rudp_socket import RudpSocket

CLI_ADDR = ('127.0.0.1', 4444)
SV_ADDR = ('127.0.0.1', 9999)
BUFSIZE = 1024

def main():
    print('init server')

    rudp = RudpSocket(CLI_ADDR)
    data, addr = rudp.recvfrom(BUFSIZE)
    rudp.close()

    print('end server')

main()
