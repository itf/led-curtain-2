#!/usr/bin/env python
import sys
from Transportation.Sockets.ServerSocketUDP import ServerSocketUDP
import Transportation.Protocol.SimpleProtocol as P
from Display.PiWS2812b.Curtain import Curtain as Curtain
try:
    import LocalConfig as Config
except:
    import Config as Config
from Config import PiDisplayConfig as PiConfig

import socket
import time

try:
    from LocalConfig import InputServerConfig as InputConfig
except:
    from Config import InputServerConfig as InputConfig

def runDisplay(host, port, height, width):
    minSleepTime=0.0000092*height*width
    #server=ServerSocketUDP(host,port)
    server = Config.ServerProtocolClass(host, port)
    curtain = Curtain(width,height)
    lastServer=["",""]

    while(1):
        try:
            isUDP = Config.whichProtocol =="UDP"
            if isUDP:
                dataRaw = server.getDataHost()
                data =dataRaw[0]
            else:
                data = server.getData()
                dataRaw = [data, ['','']] #compatibility for tcp code
            if data =="" and isUDP: #Necessary for games
                try:
                    print "empty Data"
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    newClientIP= dataRaw[1][0]
                    newClientPort = InputConfig.port 
                    sock.sendto(lastServer[0], (newClientIP,newClientPort))
                except:
                    pass
                
            else:
                lastServer=dataRaw[1]   
                curtain.sendColorCanvas(data)
                time.sleep(minSleepTime)
        except KeyboardInterrupt:
            exit()
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
        runDisplay(host, PiConfig.port, PiConfig.height, PiConfig.width)
    else:
        print "Usage Cli [host] <height> <width> <port> "

    
if __name__ == "__main__":
   main(sys.argv[1:])
