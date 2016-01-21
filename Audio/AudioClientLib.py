'''
Based on https://github.com/ervanalb/beat-off/blob/master/src/timebase/timebase.c
'''
import time
import threading

import Transportation.Sockets.ServerSocketUDP as Server
from Config import AudioServerConfig as Config

 

DEBUG = 0

class AudioInfo:
    def __init__(self, host=None, port=None, delay = None):
        self.running=True
        if host == None:
            self.host = Config.host
        if port == None: 
            self.port = Config.port
        if delay == None:
            self.delay = Config .delay
        self._alpha = Config.alpha
        self._maxBPS = Config.maxBPS
        self.socket = Server.ServerSocketUDP(self.host,self.port)
        self.previousBeatTime = time.time()
        self.previousTime = self.previousBeatTime
        self.curTime = self.previousTime 
        
        self.previousBeat = 0
        self._previousTotalBeats=0
        self.totalBeats = 0
        self.beatsPerSecond = 140./60


        #self.lock = threading.RLock()
        threadListener= threading.Thread(target=self._listenerFunction,
                                   args= ())
        threadListener.start()

    def _listenerFunction(self):
        self.socket.sock.settimeout(2)
        while self.running:
            try:
                data = self.socket.getData()
                if data=="beat":
                    self._tap()
            except:
                pass
        self.socket.sock.close()


    
    
    def _tap(self):
        #self.lock.acquire()
        if DEBUG:
            print "beat"
            print self.beatsPerSecond
        now = time.time()
        beatsPerSecond = 1./(now-self.previousBeatTime)
        if (beatsPerSecond <self._maxBPS):
            alpha=self._alpha
            self.beatsPerSecond = self.beatsPerSecond*alpha+beatsPerSecond*(1-alpha)
            self.previousBeatTime = now
            self.totalBeats+=1
        #self.lock.release()

    def getBeat(self):
        self.curTime = time.time()
        currentBeat = self._getCurrentBeat(self.curTime, self.delay)

        if currentBeat>self.previousBeat or (self.previousBeat>0.5 and currentBeat<self.previousBeat-0.5):
            self.previousBeat = currentBeat%1
        else:
            currentBeat=self.previousBeat

        self.previousTime = self.curTime
        return currentBeat%1

    def getTotalBeats(self):
        self.curTime = time.time()
        totalBeats= self._getCurrentBeat(self.curTime)+self.totalBeats
        if totalBeats > self._previousTotalBeats:
            self._previousTotalBeats = totalBeats
            return totalBeats
        else:
            beats = self._previousTotalBeats = totalBeats
            self._previousTotalBeats = totalBeats # if there is a problem it will last only for one frame
            return self._previousTotalBeats
    def getBPM(self):
        return self.beatsPerSecond*60
                
    def _getCurrentBeat(self, currentTime, delay=0):
        #self.lock.acquire()
        result = (currentTime - self.previousBeatTime-delay) * self.beatsPerSecond
        #self.lock.release()
        return result
