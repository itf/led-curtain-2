#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
from Display.Pygame.pgCurtain import PygameCurtain
import socket
import Transportation.Protocol.SimpleProtocol as P
try:
    from LocalConfig import LocalDisplayConfig as Config
except:
    from Config import LocalDisplayConfig as Config

try:
    from LocalConfig import InputServerConfig as InputConfig
except:
    from Config import InputServerConfig as InputConfig

from ColorManager import convertColorByteToS

def testServer(host, port, height, width):
    server=ServerSocketUDP(host,port)
    curtain = PygameCurtain(width,height)
    lastServer=["",""]
    while(1):
        dataRaw = server.getDataHost()
        data =dataRaw[0]
        if data =="": #Necessary for games
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                newClientIP= dataRaw[1][0]
                newClientPort = InputConfig.port 
                sock.sendto(lastServer[0], (newClientIP,newClientPort))
            except:
                pass
            
        else:
            lastServer=dataRaw[1]        
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
