import time
import curses
import Transportation.Sockets.ClientSocketUDP as Client
import Transportation.Sockets.ServerSocketUDP as Server

try:
    import LocalConfig as Config
except:
    import Config

DEBUG = 0

def inputProcess(port, host='localhost', player=1):
    clientSocket = [Client.ClientSocketUDP(host,port)]
    def sendKey(stdscr):
        while True:
            c = stdscr.getkey()
            if c == "KEY_F(5)":
                try:
                    serverSocket = Server.ServerSocketUDP('',port)
                    clientSocket2 = Client.ClientSocketUDP(Config.host,Config.port)
                    print Config.host
                    for i in xrange(100):
                        clientSocket2.sendData("")
                    serverSocket.sock.settimeout(2)
                    newIP= serverSocket.getData()
                    clientSocket[0] = Client.ClientSocketUDP(newIP,port)
                    print "New IP is " + newIP
                    serverSocket.close()
                except:
                    serverSocket.close()
                    print "Could not get new ip"

                    
            try:
                clientSocket[0].sendData(str(player)+'#'+c)
            except:
                pass
            if DEBUG:
                print c
    curses.wrapper(sendKey)



