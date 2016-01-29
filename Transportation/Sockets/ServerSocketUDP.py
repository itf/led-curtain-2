import socket
import sys
from Transportation.ServerInterface import ServerInterface as ServerInterface


class ServerSocketUDP(ServerInterface):
    def __init__(self,host,port):
        self._serverAddress = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self._serverAddress)

        
    def getData(self):
        return self.sock.recvfrom(16384)[0]
