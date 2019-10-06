import socket, os

CHUNK_SIZE = 1024

def upload_file(server_address, src, name):
  """ DOING: Implementación TCP upload_file client
  Backlog:
    * modularizar
  """
  print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

  # Creación socket TCP
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Conexión contra svr-host:svr-port
  sock.connect(server_address)

  # Envío largo nombre de archivo
  filename_size = len(name)
  bytes_sent = 0
  while bytes_sent < len(str(filename_size)):
    bytes_sent += sock.send(str(filename_size).encode())

  # Espero OK de svr
  signal = sock.recv(CHUNK_SIZE).decode()

  if signal != 'start':
    print('Error receiving name size from server')
    return exit(1)

  # Envío nombre de archivo al servidor
  bytes_sent = 0
  while bytes_sent < filename_size:
    bytes_sent += sock.send(name.encode())

  command = 'upload'
  cmd_len = len(command)
  sock.send(str(cmd_len).encode())

  # Espero OK de svr
  signal = sock.recv(CHUNK_SIZE).decode()

  if signal != 'start':
    print('Error receiving name size from server')
    return exit(1)

  bytes_sent = 0
  while bytes_sent < cmd_len:
    bytes_sent += sock.send(command.encode())

  # Envío archivo al servidor
  f = open(src, "rb")
  f.seek(0, os.SEEK_END)
  file_size = f.tell()
  f.seek(0, os.SEEK_SET)

  print("Sending {} bytes from {}".format(file_size, src))

  # Envío tamaño de archivo en bytes
  sock.send(str(file_size).encode())
  signal = sock.recv(CHUNK_SIZE)

  if signal.decode() != "start":
    print("There was an error on the server")
    return exit(1)

  bytes_sent = 0
  while bytes_sent < file_size:
    chunk = f.read(CHUNK_SIZE)
    if not chunk:
      break
    bytes_sent += sock.send(chunk)

  # Cierro archivo
  f.close()
  # Cierro socket
  sock.close()
