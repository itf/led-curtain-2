import socket
import sys
from Transportation.ClientInterface import ClientInterface as ClientInterface

class ClientSocketUDP(ClientInterface):
    def __init__(self,host,port):
        self._serverAddress = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        
    def sendData(self,data):
        sent = self.sock.sendto(data, self._serverAddress)

