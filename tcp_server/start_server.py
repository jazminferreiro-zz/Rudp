import socket

CHUNK_SIZE = 1024

def start_server(server_address, storage_dir):
  # DOING: Implementar TCP server
  # host = server_address[0]
  # port = server_address[1]
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
    filename = ''

    # TODO: ver validar cuando recibi todo el numero
    filename_size = int(conn.recv(CHUNK_SIZE).decode())
    print('filename length: {}'.format(filename_size))

    # Envío a svr OK TODO: revisar
    conn.send(b'start')

    # Recepción nombre de archivo
    bytes_recv = 0
    while bytes_recv < filename_size:
      data = conn.recv(CHUNK_SIZE).decode()
      filename += data
      bytes_recv += len(data)

    filename = "{}/{}".format(storage_dir,filename)
    print('filename: {}'.format(filename))

    f = open(filename, "wb")
    #
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

def recv_cmd():
  """ Se recibe por parte del cliente si quiere subir o descargar un archivo """
  pass