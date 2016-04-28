#!/usr/bin/python
import sys
from Config import InputServerConfig as Config
from Input import InputClientLib as InputLib


def main(argv):

    if len(argv)==3:
        InputLib.inputProcess(*argv)
    elif len(argv)==0:
        host = Config.host
        port = Config.port
        player = Config.playerNumber
        argv=[port,host,player]   
        InputLib.inputProcess(*argv)
    elif len(argv)==1:
        host = Config.host
        port = Config.port
        player = argv[0]
        argv=[port,host,player]   
        InputLib.inputProcess(*argv)
    else:
        print "Usage AudioServer <port> <host> "

if __name__ == "__main__":
   main(sys.argv[1:])

