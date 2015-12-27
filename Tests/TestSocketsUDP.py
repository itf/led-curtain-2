from Transportation.Sockets.ClientSocketUDP import ClientSocketUDP
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP

import time
import random
import threading


def main():
    host ='localhost'
    port=5000
    try:
        threadServer= threading.Thread(target=testServer, args= (host, port))
        threadClient= threading.Thread(target=testClient, args= (host, port))
        threadServer.start()
        threadClient.start()
        threadServer.join()
        threadClient.join()
    except:
        print "Error: unable to start thread"
    

def testServer(host, port):
    server=ServerSocketUDP(host,port)
    server.sock.settimeout(1)
    print server.getData()

def testClient(host, port):
    client= ClientSocketUDP(host,port)
    message = "ping"
    for i in xrange(10):
        client.sendData(message)
        time.sleep(0.1)
