import socket
import sys
from Transportation.ServerInterface import ServerInterface as ServerInterface
import thread
import time

class ServerSocketTCP(ServerInterface):
    def __init__(self,host,port):
        self.stopped = False
        self._serverAddress = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self._serverAddress)
        self.sock.listen(5)
        #Note it's (socket,) not (socket) because second parameter is a tuple
        print("create connect thread")
        thread.start_new_thread(self.createConnectionAcceptServer,(self.sock,))
        self.data = ''

    def getData(self):
        #blocking get data. May return old data/data that is partially new and old
        while(self.data == ''):
            time.sleep(0.003)
        data = self.data
        self.data = ''
        return data
    def getDataHost(self):
        pass
    def close(self):
        self.stopped = True
        self.sock.close()
    def createConnectionAcceptServer(self, s):
        while not self.stopped:
            try: 
                c, addr = s.accept()     # Establish connection with client.
            except socket.timeout:
                pass
            except:
                raise
            else:
                print('Connected to: ' + str(addr[0]) + ':' + str(addr[1]))
                thread.start_new_thread(self.on_new_client,(c,addr))
                print("create startnew thread")
                #Note it's (addr,) not (addr) because second parameter is a tuple
                #Edit: (c,addr)
                #that's how you pass arguments to functions when creating new threads using thread module.
        socket.close()
    def on_new_client(self, clientsocket, addr):
        print("start of new client")
        clientsocket.setblocking(1)
        thisStopped = False
        while not self.stopped and not thisStopped:
            msg = clientsocket.recv(16384)
            if len(msg) == 0:
                thisStopped = True
            #do some checks and if msg == someWeirdSignal: break:
            self.data = msg
        print ("closed connection")
        clientsocket.close()

