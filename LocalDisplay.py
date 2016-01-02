#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
from Display.Pygame.pgCurtain import PygameCurtain
import Transportation.Protocol.SimpleProtocol as P


def testServer(host, port, height, width):
    server=ServerSocketUDP(host,port)
    curtain = PygameCurtain(width,height)
    while(1):
        data = server.getData()
        colorArray=P.dataToColorArray(data)
        curtain.sendColorArray(colorArray)

def main(argv):
    if len(argv)==3:
        height,width,port=argv
        host ='localhost'
        testServer(host, int(port), int(height), int(width))
    elif len(argv)==0:
        host ='localhost'
        testServer(host, 5000, 30, 60)
    else:
        print "Usage Cli <height> <width> <port> "

    
if __name__ == "__main__":
   main(sys.argv[1:])
