import socket
import sys
from Transportation.ClientInterface import ClientInterface as ClientInterface

class ClientSocketUDP(ClientInterface):
    def __init__(self,host,port):
        self._serverAddress = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        
    def sendData(self,data):
        sent = self.sock.sendto(data, self._serverAddress)

