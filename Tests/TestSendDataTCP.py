from Transportation.Sockets.ClientSocketTCP import ClientSocketTCP
from Transportation.Sockets.ServerSocketTCP import ServerSocketTCP
import Transportation.Protocol.SimpleProtocol as P
from Display.Pygame.pgCurtain import PygameCurtain


import time
import random
import threading
import sys
import os

height =10
width =5
def main():
    host ='localhost'
    port=5000
    try:
        threadServer= threading.Thread(target=testServer, args= (host, port))
        threadClient= threading.Thread(target=testClient, args= (host, port))
        threadServer.start()
        threadClient.start()
        threadClient.join()
        print("joined")
        os._exit(1)
        exit()
    except:
        print "Error: unable to start thread"
    

def testServer(host, port):
    server=ServerSocketTCP(host,port)
    server.sock.settimeout(1)
    curtain = PygameCurtain(width,height)
    while(1):
        data = server.getData()
        colorArray=P.dataToColorArray(data)
        curtain.sendColorArray(colorArray)

def testClient(host, port):
    client= ClientSocketTCP(host,port)
    for i in xrange(50):
        rgb= [tuple([getRandom(),getRandom(),getRandom()]) for i in range(0, 3*height*width, 3)]
        colorArray=[rgb[i:i+width] for i in range(0, height*width, width)]
        data= P.colorArrayToData(colorArray)
        client.sendData(data)
        time.sleep(0.1)
    client.closeSocket()
    print("finished sending data")

def getRandom():
    return random.randint(0, 255)
