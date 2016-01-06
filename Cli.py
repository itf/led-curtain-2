#!/usr/bin/env python
import sys
import threading
import time
import copy
import rlcompleter
import readline


import Transportation.Protocol.SimpleProtocol as P
import Transportation.Sockets.ClientSocketUDP as Client
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import SavedPatterns


import Patterns.StaticPatterns.basicPatterns as basicPattern
from ScreenCanvas import Canvas

"""
Usage Cli <height> <width> <host> <port>

This class is a prototype with lots of poor choices(in my opinion)
"""

SEND_RATE=60

class Completer(rlcompleter.Completer):
    '''
    Modifies rlcompleter.Completer to implement autocompletion
    '''
    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
        import keyword
        matches = []
        n = len(text)
        for word in keyword.kwlist:
            if word[:n] == text:
                matches.append(word)
        for nspace in [self.namespace]:
            for word, val in nspace.items():
                if word[:n] == text:
                    matches.append(self._callable_postfix(val, word))
        return matches
    
    def _callable_postfix(self, val, word):
        if hasattr(val, '__call__') and word not in self.patternDict:
            word = word + "("
        return word
    
    def setPatternDict(self,pDict):
        self.patternDict=pDict

def savePattern(name, code):
    with open("SavedPatterns.py", "a") as savedFunctions:
        savedFunctions.write('\n' + 'Pattern.pattern(\''+name+'\')('+ code+')')
        savedFunctions.close()


def runCliCurtain(argv):
    dictAll={}
    dictAll.update(Pattern.getPatternDic())
    dictAll.update(Function.getFunctionDict())
    dictAll.update(Function.getMetaFunctionDict())
    importFunctionsFromDict(dictAll)

    readline.parse_and_bind("tab: complete")
    completer=Completer(dictAll)
    completer.setPatternDict(Pattern.getPatternDic())
    
    readline.set_completer(completer.complete)
    
    height, width, host, port = argv
    height = int(height)
    width = int(width)
    port = int(port)
    patternContainer=[basicPattern.randomPattern, None]
    patternString="random"
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
            instruction = raw_input('Pattern (p), parameter(r), List (l) or Save (s)\n')
            if instruction=="r":
                parameter = input('Please input {\'parameterName\':value} \n')
                patternInput.update(parameter)
            elif instruction=="p":
                try:
                    rawFunction = raw_input ('Please write the pattern\n')
                    function = eval(rawFunction)
                    patternString=rawFunction
                    patternContainer[1]=patternContainer[0]
                    patternContainer[0]=function
                except:
                    e = sys.exc_info()[0]
                    print e
            elif instruction =="l":
                print "PATTERNS:"
                patternDict=Pattern.getPatternDic()
                for pattern in patternDict.keys():
                    print str(pattern) +" " + str(patternDict[pattern].func_doc)

                print "\nFUNCTIONS:"
                funcDict=Function.getFunctionDict()
                for function in funcDict.keys():
                    print str(function) +" " + str(funcDict[function].func_doc)

                print "\nMETA FUNCTIONS:"
                metaFuncDict=Function.getMetaFunctionDict()
                for function in metaFuncDict.keys():
                    print str(function) +" " + str(metaFuncDict[function].func_doc)
            elif instruction =="s":
                name = raw_input('Name for previous pattern:\n')
                savePattern(name,patternString)


                
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
                newPatternInput=pattern(patternInput)
                canvas=newPatternInput["canvas"]
                data=P.canvasToData(canvas)
                clientSocket.sendData(data)
                patternInput=newPatternInput
                time.sleep(timeSleep)
            except:
                    e = sys.exc_info()[0]
                    print e
                    patternContainer[0]=patternContainer[1]



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



