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

        self.intensity = 0
        self.lowIntensity = 0

        self.lock = threading.RLock()
        threadListener= threading.Thread(target=self._listenerFunction,
                                   args= ())
        threadListener.setDaemon(True)
        threadListener.start()

    def _listenerFunction(self):
        self.socket.sock.settimeout(2)
        while self.running:
            try:
                data = self.socket.getData()
                if data=="beat":
                    self._tap()
                else:
                    type, value = data.split('#',1)
                    if type=="I":
                        self._setIntensity(value)
                    if type=="L":
                        self._setLowIntensity(value)

            except:
                pass
        self.socket.sock.close()


    def _setIntensity(self, value):
        self.intensity = float(value)

    def getIntensity(self):
        return self.intensity

    def _setLowIntensity(self, value):
        self.lowIntensity = float(value)

    def getLowIntensity(self):
        return self.lowIntensity

    
    def _tap(self):
        self.lock.acquire()
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
        self.lock.release()

    def getBeat(self, update=True):
        self.curTime = time.time()
        currentBeat = self._getCurrentBeat(self.curTime, self.delay)

        if currentBeat>self.previousBeat or (self.previousBeat>0.5 and currentBeat<self.previousBeat-0.5):
            pass
        else:
            expectedPrevious= self._getCurrentBeat(self.previousTime, self.delay)
            change = (currentBeat-expectedPrevious)
            newCurrent = change/4 + self.previousBeat
            if newCurrent > self.previousBeat:
                currentBeat=newCurrent
            else:
                currentBeat=self.previousBeat

        self.previousTime = self.curTime
        self.previousBeat = currentBeat%1
        return self.previousBeat

    def getTotalBeats(self):
        self.lock.acquire()
        self.curTime = time.time()
        totalBeats= self._getCurrentBeat(self.curTime)+self.totalBeats
        if totalBeats >= self._previousTotalBeats:
            self._previousTotalBeats = totalBeats
        else:
            #this means that beat detection is working and therefore self._getCurrentBeat<1
            if self.totalBeats<int(self._previousTotalBeats)-2:
                self.lock.acquire()
                self.totalBeats = int(self._previousTotalBeats)
                self.lock.release()

            currentBeat = self._getCurrentBeat(self.curTime, self.delay)
            expectedPrevious= self._getCurrentBeat(self.previousTime, self.delay)
            change = (currentBeat-expectedPrevious)%1
            newCurrent = change/4 + self.previousBeat+self.totalBeats
            if newCurrent > self._previousTotalBeats:
                totalBeats=newCurrent
            else:
                totalBeats=self._previousTotalBeats
            self.previousTime = self.curTime
            self._previousTotalBeats = totalBeats
        self.lock.release()
        return self._previousTotalBeats
    def getBPM(self):
        return self.beatsPerSecond*60
                
    def _getCurrentBeat(self, currentTime, delay=0):
        self.lock.acquire()
        result = (currentTime - self.previousBeatTime-delay) * self.beatsPerSecond
        self.lock.release()
        return result
