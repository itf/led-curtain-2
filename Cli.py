#!/usr/bin/env python
import sys
import threading
import time

import Transportation.Protocol.SimpleProtocol as P
import Transportation.Sockets.ClientSocketUDP as Client
import Patterns.Pattern as Pattern
import Patterns.Function as Function


import Patterns.StaticPatterns.basicPatterns as basicPattern
from ScreenCanvas import Canvas

"""
Usage Cli <height> <width> <host> <port>

This class is a prototype with lots of poor choices(in my opinion)
"""

SEND_RATE=60


def runCliCurtain(argv):
    importFunctionsFromDict(Pattern.getPatternDic())
    importFunctionsFromDict(Function.getFunctionDict())
    height, width, host, port = argv
    height = int(height)
    width = int(width)
    port = int(port)
    patternContainer=[basicPattern.randomPattern]
    patternInput = Pattern.PatternInput(height=height, width = width)
    canvas = Canvas(height=height, width=width)
    patternInput["canvas"]=canvas
    threadSender= threading.Thread(target=dataSender,
                                   args= (patternContainer,
                                          patternInput,
                                          host,
                                          port))
    threadSender.start()
    while(patternContainer[0]):
        try:
            instruction = raw_input('Pattern (p), parameter(r) or List (l)')
            if instruction=="r":
                parameter = input('Please input {\'parameterName\':value} ')
                patternInput.update(parameter)
            elif instruction=="p":
                function = input ('Please write the pattern')
                patternContainer[0]=function
            elif instruction =="l":
                print "PATTERNS:"
                patternDict=Pattern.getPatternDic()
                for pattern in patternDict.keys():
                    print str(pattern) +" " + str(patternDict[pattern].func_doc)

                print "\nFUNCTIONS:"
                funcDict=Function.getFunctionDict()
                for function in funcDict.keys():
                    print str(function) +" " + str(funcDict[function].func_doc)
                
        except KeyboardInterrupt:
            patternContainer[0]=None
            threadSender.join()
            print "threads successfully closed"

def dataSender(patternContainer, patternInput, host, port):
    height = patternInput["height"]
    width = patternInput["width"]
    canvas = Canvas(height,width)
    patternInput["canvas"]=canvas
    frame=0
    previousPattern=patternContainer[0]

    clientSocket = Client.ClientSocketUDP(host,port)
    timeSleep = 1.0/SEND_RATE
    errorSleep= 3
    while patternContainer[0]:
        try:
            pattern=patternContainer[0]
            if(pattern!=previousPattern):
                frame=0
                previousPattern=pattern
            else:
                frame = frame+1
            patternInput["frame"]=frame
            canvas=pattern(patternInput)["canvas"]
            data=P.canvasToData(canvas)
            clientSocket.sendData(data)
            patternInput.canvas=canvas
            time.sleep(timeSleep)
        except:
            print "Malformed pattern"
            time.sleep(3)



def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

def main(argv):

    if len(argv)==4:
        runCliCurtain(argv)
    elif len(argv)==0:
        argv=[30,60,'localhost',5000]
        runCliCurtain(argv)
    else:
        print "Usage Cli <height> <width> <host> <port> "

if __name__ == "__main__":
   main(sys.argv[1:])
