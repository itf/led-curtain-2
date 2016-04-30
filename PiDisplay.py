#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
import Transportation.Protocol.SimpleProtocol as P
from Display.PiWS2812b.Curtain import Curtain as Curtain
from Config import PiDisplayConfig as Config
import time

try:
    from LocalConfig import InputServerConfig as InputConfig
except:
    from Config import InputServerConfig as InputConfig

def runDisplay(host, port, height, width):
    minSleepTime=0.0000090*height*width
    server=ServerSocketUDP(host,port)
    curtain = Curtain(width,height)
    lastServer=["",""]

    while(1):
        try:
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
                data = server.getData()
                curtain.sendColorCanvas(data)
                time.sleep(minSleepTime)
        except:
            pass


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
