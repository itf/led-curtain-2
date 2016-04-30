'''
Based on https://github.com/ervanalb/beat-off/blob/master/src/timebase/timebase.c
'''
import time
import threading

import Transportation.Sockets.ServerSocketUDP as Server
from Config import InputServerConfig as Config

 

DEBUG = 0

#Inputs get deleted every 18 seconds.
LOGOUT_TIME=18
#Input list only keeps track of the last 10 inputs
MAX_INPUT_LIST=10
#Keeping input list and last inputs is redundant, but it makes it easier to use.
#Last input is for games such as snake, while input list for games where you have the option not to move
###
class InputInfo:
    def __init__(self, host=None, port=None):
        self.running=True
        if host == None:
            self.host = Config.server
        if port == None: 
            self.port = Config.port
        self.socket = Server.ServerSocketUDP(self.host,self.port)

        self.input={}
        self.inputList={}
        self.inputTime={}

        self.lock = threading.RLock()
        threadListener= threading.Thread(target=self._listenerFunction,
                                   args= ())
        threadListener.start()

    def _listenerFunction(self):
        self.socket.sock.settimeout(2)
        while self.running:
            try:
                data = self.socket.getData()
                player, command = data.split('#')
                self.lock.acquire()
                self.input[player]=command
                if self.inputList.has_key(player):
                    playerList= self.inputList[player]
                    playerList.append(command)
                    if len(playerList)==MAX_INPUT_LIST:
                        try:
                            playerList.pop(0)
                        except:
                            pass
                else:
                    self.inputList[player] = [command]
                self.inputTime[player]=time.time()
                self.lock.release()
            except:
                pass
        self.socket.sock.close()



# The 2 following functions are mostly redundant
#
    def getLastInputs(self):
        curTime=time.time()
        self.lock.acquire()
        kill=[]
        for i in self.inputTime:
            if self.inputTime[i] < curTime-LOGOUT_TIME:
                kill.append(i)
        for i in kill:
            self.inputTime.pop(i)
            self.inputList.pop(i)
            self.input.pop(i)
        self.lock.release()
        return self.input

    def getInputList(self):
        curTime=time.time()
        self.lock.acquire()
        kill=[]
        for i in self.inputTime:
            if self.inputTime[i] < curTime-LOGOUT_TIME:
                kill.append(i)
        for i in kill:
            self.inputTime.pop(i)
            self.inputList.pop(i)
            self.input.pop(i)
        self.lock.release()
        return self.inputList


