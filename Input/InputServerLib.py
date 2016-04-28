'''
Based on https://github.com/ervanalb/beat-off/blob/master/src/timebase/timebase.c
'''
import time
import threading

import Transportation.Sockets.ServerSocketUDP as Server
from Config import InputServerConfig as Config

 

DEBUG = 0

#Inputs get deleted every 10 seconds.
class InputInfo:
    def __init__(self, host=None, port=None):
        self.running=True
        if host == None:
            self.host = Config.host
        if port == None: 
            self.port = Config.port
        self.socket = Server.ServerSocketUDP(self.host,self.port)

        self.input={}
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
                self.inputTime[player]=time.time()
                self.lock.release()
            except:
                pass
        self.socket.sock.close()


    
    def getInputs(self):
        curTime=time.time()
        self.lock.acquire()
        kill=[]
        for i in self.inputTime:
            if self.inputTime[i] < curTime-10:
                kill.append(i)
        for i in kill:
            self.inputTime.pop(i)
            self.input.pop(i)
        self.lock.release()
        return self.input


