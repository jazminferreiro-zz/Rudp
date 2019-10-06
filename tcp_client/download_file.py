import socket

CHUNK_SIZE = 1024

def download_file(server_address, name, dst):
  """ DOING: Implementar TCP download_file client
  Backlog:
    * modularizar
  """
  print('TCP: download_file({}, {}, {})'.format(server_address, name, dst))

  # Creación socket TCP
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Conexión contra svr-host:svr-port
  sock.connect(server_address)

  # Envío largo nombre de archivo
  filename_size = len(name)

  bytes_sent = 0
  while bytes_sent < len(str(filename_size)):
    bytes_sent += sock.send(str(filename_size).encode())

  signal = sock.recv(CHUNK_SIZE).decode()

  if signal != 'start':
    print('Error receiving name size from server')
    return exit(1)
  else:
    print("signal: {}".format(signal))

  # Envío nombre de archivo al servidor
  bytes_sent = 0
  while bytes_sent < filename_size:
    bytes_sent += sock.send(name.encode())

  f = open(dst, "wb")

  # Recepción cantidad de bytes de archivo
  file_size = int(sock.recv(CHUNK_SIZE).decode())

  print("filesize: {}".format(file_size))
  sock.send(b'start')

  bytes_recv = 0
  while bytes_recv < file_size:
    data = sock.recv(CHUNK_SIZE)
    bytes_recv += len(data)
    f.write(data)

  f.close()
  print("Received file {}".format(dst))

  sock.close()
