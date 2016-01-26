#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
import Transportation.Protocol.SimpleProtocol as P
from Display.PiWS2812b.Curtain import Curtain as Curtain
from Config import PiDisplayConfig as Config

def runDisplay(host, port, height, width):
    server=ServerSocketUDP(host,port)
    curtain = PygameCurtain(width,height)
    while(1):
        data = server.getData()
        colorArray=P.dataToColorArray(data)
        curtain.sendColorArray(colorArray)

def main(argv):
    if len(argv)==4:
        host, height,width,port=argv
        runDisplay(host, int(port), int(height), int(width))
    if len(argv)==3:
        height,width,port=argv
        host =''
        runDisplay(host, int(port), int(height), int(width))
    elif len(argv)==0:
        host =''
        runDisplay(host, Config.port, Config.height, Config.width)
    else:
        print "Usage Cli [host] <height> <width> <port> "

    
if __name__ == "__main__":
   main(sys.argv[1:])
