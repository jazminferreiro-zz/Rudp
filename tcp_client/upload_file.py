import socket

def upload_file(server_address, src, name):
  # TODO: Implementar TCP upload_file client
  print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

  # Se crea socket TCP
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Conexión contra svr-host:svr-port
  sock.connect(server_address)

  sock.close()
