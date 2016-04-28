import time
import curses
import Transportation.Sockets.ClientSocketUDP as Client
from Config import InputServerConfig as Config

DEBUG = 1

def inputProcess(port, host='localhost', player=1):
    clientSocket = Client.ClientSocketUDP(host,port)
    clientSocket.sendData("beat")
    def sendKey(stdscr):
        while True:
            c = stdscr.getkey()
            try:
                clientSocket.sendData(str(player)+'#'+c)
            except:
                pass
            if DEBUG:
                print c
    curses.wrapper(sendKey)



