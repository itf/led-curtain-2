import socket
import sys
from Transportation.ClientInterface import ClientInterface as ClientInterface



class ClientSocketTCP(ClientInterface):
    def __init__(self,host,port):
        self.ip = host
        self._serverAddress = (self.ip , port)
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect(self._serverAddress)

        
    def sendData(self,data):
        sent = self.sock.sendall(data)

    def closeSocket(self):
        self.sock.close()
