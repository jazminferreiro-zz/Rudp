import socket

CHUNK_SIZE = 1024
NUM_SIZE = 10

"""
Socket TCP
envia y recibe bytes
"""
class TcpSocket:
  def __init__(self, server_address: tuple, is_connected: bool = False, conn_socket = None):
      # Creación socket TCP
      self.server_address = server_address
      self.is_connected = is_connected
      if(self.is_connected and conn_socket != None):
          self.sock = conn_socket
      else:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  def bind_and_listen(self) :
      # Bind socket a host:port
      self.sock.bind(self.server_address)
      # Se prepara para aceptar conexiones - TODO: por ahora 1 cliente
      self.sock.listen(1)

  def accept(self) -> 'TcpSocket':
      conn_sock, addr_info = self.sock.accept()
      if not conn_sock:
          print("Not connected")
          raise RuntimeError("socket error accepting connection")
      self.is_connected = True
      print("Accepted connection from {}".format(addr_info))
      return TcpSocket(self.server_address, self.is_connected,conn_sock)

  def connect(self) :
      self.sock.connect(self.server_address)
      self.is_connected = True

  def stop(self):
      self.sock.shutdown(socket.SHUT_RDWR)
      self.sock.close()
      self.is_connected = False


  def send_bytes(self, msg: bytes)-> int:
      if not self.is_connected:
          raise RuntimeError("socket not connected")
      msg_len = len(msg)
      total_sent = 0
      while total_sent < msg_len:
          sent = self.sock.send(msg[total_sent:])
          if sent == 0:
              print("Error sending msg")
              raise RuntimeError("socket connection broken")
          total_sent = total_sent + sent
      return total_sent


  def receive_bytes(self, size: int)-> bytes:
      if not self.is_connected:
          raise RuntimeError("socket not connected")
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