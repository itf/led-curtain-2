#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
from Display.Pygame.pgCurtain import PygameCurtain
import Transportation.Protocol.SimpleProtocol as P
from ColorManager import convertColorByteToS
from Config import LocalDisplayConfig as Config

def testServer(host, port, height, width):
    server=ServerSocketUDP(host,port)
    curtain = PygameCurtain(width,height)
    while(1):
        data = server.getData()
        colorArray=P.dataToColorArray(data)
        if Config.linearColorProfileCorretion:
            colorArray=map(lambda y: map(lambda x:convertColorByteToS(x),y),colorArray)
        if Config.normalize:
            brightest= max ([1]+[c for row in colorArray  for color in row for c in color ])
            def normalize((r,g,b)):
                r = int(r*255./brightest)
                g = int(g*255./brightest)
                b = int(b*255./brightest)
                return tuple([r,g,b])
            colorArray=map(lambda y: map(lambda x: normalize(x) ,y), colorArray)
        curtain.sendColorArray(colorArray)

def main(argv):
    if len(argv)==4:
        host, height,width,port=argv
        testServer(host, int(port), int(height), int(width))
    if len(argv)==3:
        height,width,port=argv
        host =''
        testServer(host, int(port), int(height), int(width))
    elif len(argv)==0:
        host =''
        testServer(host, Config.port, Config.height, Config.width)
    else:
        print "Usage Cli [host] <height> <width> <port> "

    
if __name__ == "__main__":
   main(sys.argv[1:])
