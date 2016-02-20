'''
All the code necessary to make a useful UI
'''
import sys
import threading
import time
import copy
import traceback


try:
    import LocalConfig as Config
except:
    import Config
if Config.useAudio:
    import Audio.AudioClientLib as Audio

import Transportation.Sockets.ClientSocketUDP as Client
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import SavedPatterns
import SavedFunctions


import Patterns.StaticPatterns.basicPatterns as basicPattern
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import Patterns.ExtraPatterns.StatePatterns as StatePatterns



Canvas = Config.Canvas

"""
Usage Cli <height> <width> <host> <port>

This file is a prototype with lots of poor choices(in my opinion)
It is just something that was hacked together. The rest of the code doesn't reflect this file
"""

############################
#Helper functions for saving
def savePattern(name, code):
    realCode ='\n' + name.replace(" ", "") + ' = Pattern.pattern(\''+name.replace(" ", "")+'\')('+ code+')'
    with open("SavedPatterns.py", "a") as savedFunctions:
        savedFunctions.write(realCode)
        savedFunctions.close()
    return realCode

def safeSavePattern(name, code):
    realCode=savePattern(name, 'isolateCanvas('+code+')')
    return realCode

def saveFunction(name,code, patternInput):
    realFunctionCode = \
                     '@Function.function(\'' + name.replace(" ", "") + '\')\n'\
                     'def '+ name.replace(" ", "") + '(pattern):'\
                     '  return '+ code\
                     +'\n'
    exec realFunctionCode in globals(), globals()
    try:
        testPatternInput = copy.deepcopy(patternInput)
        globals()[name](trivial)(testPatternInput)
        with open("SavedFunctions.py", "a") as savedFunctions:
            savedFunctions.write(realFunctionCode)
            savedFunctions.close()
    except:
        traceback.print_exc(file=sys.stdout)
    return realFunctionCode


def createInitialPatternInput(height, width):
    patternInput = Pattern.PatternInput(height=height, width = width)
    canvas = Canvas(height,width) 
    patternInput["canvas"]=canvas
    return patternInput
    

def getDictOfFunctions():
    dictAll={}
    dictAll.update(Pattern.getPatternDic())
    dictAll.update(Function.getFunctionDict())
    dictAll.update(Function.getMetaFunctionDict())
    dictAll.update(StatePatterns.getStatePatternDic())
    return dictAll

def importFunctionsFromDict(dictionary): 
    '''
    SHOULD BE COPIED AND PASTED inside the module
    that  will call it, otherwise it won't work
    '''
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

def startSendData(host,
                  port,
                  sendRate,
                  patternContainer, #modified by the UI
                  rContainer, #modified by the UI and sender
                  rrContainer, #modified by the UI and sender
                  patternInputContainer, #Should never be modified by the UI
                  resetFrameContainer, #Should be set to 'true' every time 
                                        #a pattern is set even if it is the
                                        #same pattern
                  isClosed, #Modified by the UI
                  colorConverter, #Converts colors between colorspaces
                  canvasToData #Convers canvas to data
                  ): 
    threadSender= threading.Thread(target=_sendDataThread,
                                   args=(host,
                                         port,
                                         sendRate,
                                         patternContainer,
                                         rContainer,
                                         rrContainer,
                                         patternInputContainer,
                                         resetFrameContainer,
                                         isClosed,
                                         colorConverter,
                                         canvasToData))
    threadSender.start()
    return threadSender

def _sendDataThread(host,
                    port,
                    sendRate,
                    patternContainer,
                    rContainer,
                    rrContainer,
                    patternInputContainer,
                    resetFrameContainer,
                    isClosed,
                    colorConverter,
                    canvasToData):
    
    patternInput = patternInputContainer[0]
    frame=0
    previousPattern=patternContainer[0]
    previousPreviousPattern = previousPattern

    if Config.useAudio:
        audio = Audio.AudioInfo()
        patternInput["beat"] = audio.getBeat
        patternInput["totalBeats"] = audio.getTotalBeats
        patternInput["bpm"] = audio.getBPM

    clientSocket = Client.ClientSocketUDP(host,port)
    timeSleep = 1.0/sendRate
    previousTime = time.time()
    while patternContainer[0] and not isClosed():
            try:
                if (rContainer[0]):
                    try:
                        command = rContainer[0]
                        Function.execInPattern(command, patternInput)
                        rContainer[0]=None
                    except:
                        rContainer[0]=None
                        traceback.print_exc(file=sys.stdout)
                if (rrContainer[0]):
                    try:
                        command = rrContainer[0]
                        Function.execInPattern(command, patternInput)
                    except:
                        rrContainer[0]=None
                        traceback.print_exc(file = sys.stdout)

                pattern = patternContainer[0]
                if(pattern != previousPattern):
                    patternInput['previousPattern'] = previousPattern
                    patternInput['previousFrame'] = frame
                    frame=0
                    previousPreviousPattern = previousPattern
                    previousPattern = pattern
                    resetFrameContainer[0] = False
                elif resetFrameContainer[0]:
                    patternInput['previousPattern'] = previousPattern
                    patternInput['previousFrame'] = frame
                    frame=0
                    resetFrameContainer[0]=False
                else:
                    frame = frame+1
                patternInput["frame"]=frame
                newPatternInput=pattern(patternInput)
                canvas=copy.deepcopy(newPatternInput["canvas"])
                globalBrightness = newPatternInput['globalBrightness']
                if colorConverter:
                    canvas.mapFunction(lambda rgb,y,x: colorConverter(rgb,globalBrightness))
                data=canvasToData(canvas)
                clientSocket.sendData(data)
                patternInput=newPatternInput
                patternInputContainer[0]=patternInput
                while previousTime+timeSleep > time.time():
                    time.sleep(timeSleep/20.) #sleeps for a bit
                previousTime=time.time()
            except:
                traceback.print_exc(file = sys.stdout)
                if previousPreviousPattern:
                    patternContainer[0] = previousPreviousPattern
                    previousPreviousPattern = None
                    
                else:
                    if patternContainer[0] == basicPattern.black:
                        patternContainer[0]=None
                    height = patternInput["height"]
                    width = patternInput["width"]
                    patternInput = Pattern.PatternInput(height = height, width = width)
                    canvas = Canvas(height,width)
                    patternInput["canvas"] = canvas
                    patternInputContainer[0] = patternInput
                    rrContainer[0] = None
                    rrContainer[0] = None
                    patternContainer[0] = basicPattern.black
                    time.sleep(0.2)

    #if not running, close audio
    if Config.useAudio:
        audio.running=False



