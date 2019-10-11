import socket

CHUNK_SIZE = 1024

"""
Socket TCP
envia y recibe bytes
"""
class TCP_Socket:
  def __init__(self, server_address):
      # Creación socket TCP
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_address = server_address
      self.is_connected = False

  def _init(self, conn_socket):
      self.sock = conn_socket
      self.is_connected = True


  def bind_and_listen(self):
      # Bind socket a host:port
      self.sock.bind(self.server_address)
      # Se prepara para aceptar conexiones - TODO: por ahora 1 cliente
      self.sock.listen(1)

  def accept(self) -> 'TCP_Socket':
      conn_sock, addr_info = self.sock.accept()
      if not conn_sock:
          print("Not connected")
          raise RuntimeError("socket error accepting connection")
      self.is_connected = True
      print("Accepted connection from {}".format(addr_info))
      return TCP_Socket(conn_sock)

  def connect(self) :
      self.sock.connect(self.server_address)
      self.is_connected = True

  def stop(self):
      self.sock.shutdown(socket.SHUT_RDWR)
      self.sock.close()
      self.is_connected = False


  def send_bytes(self, msg: bytes):
      msg_len = len(msg)
      total_sent = 0
      while total_sent < msg_len:
          sent = self.sock.send(msg[total_sent:])
          if sent == 0:
              print("Error sending msg")
              raise RuntimeError("socket connection broken")
          total_sent = total_sent + sent


  def receive_bytes(self, size: int)-> bytes:
      chunks = []
      bytes_recd = 0
      while bytes_recd < size:
          chunk = self.sock.recv(min(size - bytes_recd, CHUNK_SIZE))
          if chunk == '':
              print("Error receiving msg")
              raise RuntimeError("socket connection broken")
          chunks.append(chunk)
          bytes_recd = bytes_recd + len(chunk)
      return b''.join(chunks)