import socket

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

  sock.close()
