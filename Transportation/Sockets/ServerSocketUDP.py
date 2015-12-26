import socket
import sys
from SocketInterface import SocketInterface as SocketInterface

class ServerSocketUDP(SocketInterface):
    def __init__(self,host,port):
        self._serverAddress = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(server_address)

        
    def getData(self):
        return self.sock.recvfrom(4096)
