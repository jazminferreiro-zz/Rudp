import socket, os

CHUNK_SIZE = 1024

def create_dir(storage_dir):
  if not os.path.exists(storage_dir):
    os.mkdir(storage_dir)
    print('Dir: {} created!'.format(storage_dir)) 

def recieve(conn,size):
  full_data = ''
  bytes_recv = 0
  while bytes_recv < size:
    data = conn.recv(CHUNK_SIZE).decode()
    full_data += data
    bytes_recv += len(data)
  return full_data

def start_server(server_address, storage_dir):
  """ DOING: Implementación TCP server
  Backlog:
    * modularizar
    * clase socket? 
  """
  # host = server_address[0]
  # port = server_address[1]

  create_dir(storage_dir)

  print('TCP: start_server({}, {})'.format(server_address, storage_dir))

  # Se crea socket TCP
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Se bindea socket a host:port
  sock.bind(server_address)

  # Se prepara para aceptar conexiones - TODO: por ahora 1 cliente
  sock.listen(1)

  while True:
    conn, addr_info = sock.accept()
    if not conn:
      break

    print("Accepted connection from {}".format(addr_info))

    # Recibo file_name length
    # TODO: ver validar cuando recibi todo el numero
    filename_size = int(conn.recv(CHUNK_SIZE).decode())
    print('filename length: {}'.format(filename_size))

    # Envío a svr OK TODO: revisar
    conn.send(b'start')

    # Recepción nombre de archivo
    filename = recieve(conn,filename_size)
    filename = "{}/{}".format(storage_dir,filename)
    print('filename: {}'.format(filename))

    # Recibo comando (download o upload)
    cmd_length = int(conn.recv(CHUNK_SIZE).decode())
    conn.send(b'start')
    command = recieve(conn,cmd_length)

    if command == 'download':
      # Envío de archivo al cliente
      f = open(filename, "rb")
      f.seek(0, os.SEEK_END)
      file_size = f.tell()
      f.seek(0, os.SEEK_SET)

      print("Sending {} bytes from {}".format(file_size, filename))

      # Envío tamaño de archivo en bytes
      conn.send(str(file_size).encode())
      signal = conn.recv(CHUNK_SIZE).decode()

      if signal != "start":
        print("There was an error on the server")
        return exit(1)

      bytes_sent = 0
      while bytes_sent < file_size:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
          break
        bytes_sent += conn.send(chunk)

      # Cierro archivo
      f.close()
    elif command == 'upload':
      # Recepción cantidad de bytes de archivo
      f = open(filename, "wb")

      file_size = int(conn.recv(CHUNK_SIZE).decode())
      conn.send(b'start')

      bytes_recv = 0
      while bytes_recv < file_size:
        data = conn.recv(CHUNK_SIZE)
        bytes_recv += len(data)
        f.write(data)

      f.close()
      print("Received file {}".format(filename))

  sock.close()
