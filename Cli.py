#!/usr/bin/env python
import sys
import threading
import time
import copy
import rlcompleter
import readline
import traceback

import Config
P = Config.Protocol
colorConverter= Config.convertColor
import Transportation.Sockets.ClientSocketUDP as Client
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import SavedPatterns


import Patterns.StaticPatterns.basicPatterns as basicPattern
from ScreenCanvasArray import Canvas

"""
Usage Cli <height> <width> <host> <port>

This file is a prototype with lots of poor choices(in my opinion)
It is just something that was hacked together. The rest of the code doesn't reflect this file
"""

SEND_RATE=30

class Completer(rlcompleter.Completer):
    '''
    Modifies rlcompleter.Completer to implement autocompletion
    '''
    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
        pos=readline.get_begidx()
        line=readline.get_line_buffer()
        nQuotes=line[0:pos].count("'")
        isR=len(line)>1 and line[0]=='r' and (line[1]==' ' or (len(line)>2 and line[1]=='r' and line[2]==' '))
        matches = []
        n = len(text)
        if(nQuotes%2==1 or isR):
            nspace = self.parameterDictContainer[0]
            for word, val in nspace.items():
                if word[:n] == text:
                    matches.append(self._arg_postfix(self._callable_postfix(val, word)))
            return matches
        else:
            for nspace in [self.namespace]:
                for word, val in nspace.items():
                    if word[:n] == text:
                        matches.append(self._arg_postfix(self._callable_postfix(val, word)))
            return matches

    
    def _callable_postfix(self, val, word):
        if hasattr(val, '__call__') and word not in self.patternDict:
            word = word + "("
        return word
    def _arg_postfix(self, word):
        if word=='arg(':
            word = word + "' ')("
        return word
    
    def setPatternDict(self,pDict):
        self.patternDict=pDict
        
    def setParameterDictContainer(self,pDictContainer):
        self.parameterDictContainer=pDictContainer

def savePattern(name, code):
    realCode ='\n' + name + ' = Pattern.pattern(\''+name+'\')('+ code+')'
    with open("SavedPatterns.py", "a") as savedFunctions:
        savedFunctions.write(realCode)
        savedFunctions.close()
    return realCode
def safeSavePattern(name, code):
    realCode=savePattern(name, 'isolateCanvas('+code+')')
    return realCode

def runCliCurtain(argv):
    print 
    print "CLI to combine patterns"
    print "Press TAB for completion and suggestions"
    print "If running in Python press CTRL+A for all commands"
    print 
    
    dictAll={}
    dictAll.update(Pattern.getPatternDic())
    dictAll.update(Function.getFunctionDict())
    dictAll.update(Function.getMetaFunctionDict())
    importFunctionsFromDict(dictAll)

    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind('"\C-r": reverse-search-history')
    readline.parse_and_bind('"\C-a" complete')
    readline.parse_and_bind('set menu-complete-display-prefix on')
    readline.parse_and_bind('set skip-completed-text on')
    readline.parse_and_bind('set completion-ignore-case on')
    readline.parse_and_bind('set blink-matching-paren on')
    completer=Completer(dictAll)
    completer.setPatternDict(Pattern.getPatternDic())
    try:
        readline.read_history_file('./.history')
    except:
        pass
    
    readline.set_completer(completer.complete)
    
    height, width, host, port = argv
    height = int(height)
    width = int(width)
    port = int(port)
    patternContainer=[basicPattern.randomPattern, None]
    patternString="random"
    patternInput = Pattern.PatternInput(height=height, width = width)
    patternInputContainer=[patternInput, None, None]
    threadSender= threading.Thread(target=dataSender,
                                   args= (patternContainer,
                                          patternInputContainer,
                                          host,
                                          port))
    threadSender.start()
    completer.setParameterDictContainer(patternInputContainer)
    while(patternContainer[0]):
        try:
            instruction = raw_input('Write pattern code, parameter(r), recurrentParameter(rr), List (l), Save (s) or Safe Save (ss)\n')
            readline.write_history_file('./.history')

            try:
                if instruction:
                    leftP = instruction.count('(')
                    rightP = instruction.count(')')
                    if(leftP > rightP):
                        print "Attempting to fix mismatched left parenthesis"
                        instruction=instruction+ ')'*(leftP-rightP)
                    elif (rightP>leftP):
                        print "Attempting to fix mismatched right parenthesis"
                        instruction='('*(rightP-leftP) +instruction

                    if len(instruction)>1 and instruction[0]=="r" and instruction[1]==' ':
                        command = instruction[2:]
                        patternInputContainer[1]=command
                    elif len(instruction)>2 and instruction[0]=="r" and instruction[1]=='r' and instruction[2]==' ':
                        command = instruction[3:]
                        patternInputContainer[2]=command
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
                    elif instruction =="s" or instruction =="ss":
                        name = raw_input('Name for previous pattern:\n')
                        if instruction=="s":
                            exec savePattern(name,patternString)
                            globals()[name] = patternContainer[0]
                            dictAll[name]=globals()[name]
                            
                        else:
                            exec safeSavePattern(name,patternString)
                            globals()[name] = isolateCanvas(patternContainer[0])
                            dictAll[name]=globals()[name]
                        
                    else:
                            function = eval(instruction)
                            patternString=instruction
                            patternContainer[1]=patternContainer[0]
                            patternContainer[0]=function
            except:
                traceback.print_exc(file=sys.stdout)


                
        except KeyboardInterrupt:
            patternContainer[0]=None
            threadSender.join()
            print "threads successfully closed"

def dataSender(patternContainer, patternInputContainer, host, port):
    patternInput = patternInputContainer[0]
    height = patternInput["height"]
    width = patternInput["width"]
    canvas = Canvas(height,width) 
    patternInput["canvas"]=canvas
    frame=0
    previousPattern=patternContainer[0]

    clientSocket = Client.ClientSocketUDP(host,port)
    timeSleep = 1.0/SEND_RATE
    while patternContainer[0]:
            try:
                if (patternInputContainer[1]):
                    try:
                        command = patternInputContainer[1]
                        Function.execInPattern(command, patternInput)
                        patternInputContainer[1]=None
                    except:
                        patternInputContainer[1]=None
                        traceback.print_exc(file=sys.stdout)
                if (patternInputContainer[2]):
                    try:
                        command = patternInputContainer[2]
                        Function.execInPattern(command, patternInput)
                    except:
                        patternInputContainer[2]=None
                        traceback.print_exc(file=sys.stdout)

                pattern=patternContainer[0]
                if(pattern!=previousPattern):
                    frame=0
                    previousPattern=pattern
                else:
                    frame = frame+1
                patternInput["frame"]=frame
                newPatternInput=pattern(patternInput)
                canvas=copy.deepcopy(newPatternInput["canvas"])
                globalBrightness = newPatternInput['globalBrightness']
                if colorConverter:
                    canvas.mapFunction(lambda rgb,y,x: colorConverter(rgb,globalBrightness))
                data=P.canvasToData(canvas)
                clientSocket.sendData(data)
                patternInput=newPatternInput
                patternInputContainer[0]=patternInput
                time.sleep(timeSleep)
            except:
                traceback.print_exc(file=sys.stdout)
                patternContainer[0]=patternContainer[1]



def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

def main(argv):

    if len(argv)==4:
        runCliCurtain(argv)
    elif len(argv)==0:
        height = Config.height
        width = Config.width
        host = Config.host
        port = Config.port
        argv=[height, width, host, port]   
        runCliCurtain(argv)
    else:
        print "Usage Cli <height> <width> <host> <port> "

if __name__ == "__main__":
   main(sys.argv[1:])



