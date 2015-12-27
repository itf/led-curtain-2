from Transportation.Sockets.ClientSocketUDP import ClientSocketUDP
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
import Transportation.Protocol.SimpleProtocol as P
from Display.Pygame.pgCurtain import PygameCurtain


import time
import random
import threading

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
    except:
        print "Error: unable to start thread"
    

def testServer(host, port):
    server=ServerSocketUDP(host,port)
    server.sock.settimeout(1)
    curtain = PygameCurtain(width,height)
    while(1):
        data = server.getData()
        colorArray=P.dataToColorArray(data)
        curtain.sendColorArray(colorArray)

def testClient(host, port):
    client= ClientSocketUDP(host,port)
    for i in xrange(50):
        rgb= [tuple([getRandom(),getRandom(),getRandom()]) for i in range(0, 3*height*width, 3)]
        colorArray=[rgb[i:i+width] for i in range(0, height*width, width)]
        data= P.colorArrayToData(colorArray)
        client.sendData(data)
        time.sleep(0.2)

def getRandom():
    return random.randint(0, 255)
