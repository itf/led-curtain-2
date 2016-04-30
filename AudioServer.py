#!/usr/bin/python
import sys

import Transportation.Sockets.ClientSocketUDP as Client
try:
    from LocalConfig import AudioServerConfig as Config
except:
    from Config import AudioServerConfig as Config

    

from Audio import AudioServerLib as AudioLib


def main(argv):

    if len(argv)==2:
        AudioLib.audioProcess(*argv)
    elif len(argv)==1:
        port = argv[0]
        host = Config.host
        argv=[port,host]   
        AudioLib.audioProcess(*argv)
    elif len(argv)==0:
        host = Config.host
        port = Config.port
        argv=[port,host]   
        AudioLib.audioProcess(*argv)
    else:
        print "Usage AudioServer <port> <host> "

if __name__ == "__main__":
   main(sys.argv[1:])

