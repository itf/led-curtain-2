#!/usr/bin/env python
import sys
import threading
import time
import copy

##Throws an exception when running under pypy on windows
#Still runs the code, but with limited functionality
try:
    import rlcompleter
    import readline
except:
    print "Running CLI without readline."
    class readline_class():
        def __getattr__(self, attr):
            return lambda *args, **vargs: None

        def __setattr__(self, key, value):
            return True
    readline = readline_class()

import traceback
import re

import Config
try:
    import LocalConfig as Config
except:
    pass
P = Config.Protocol
colorConverter= Config.convertColor

import Patterns.Pattern as Pattern
import Patterns.Function as Function


import Patterns.StaticPatterns.basicPatterns as basicPattern
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import Patterns.ExtraPatterns.StatePatterns as StatePatterns
import Patterns.ExtraPatterns.HuslColor

import UI.UIUtils as UIUtils


Canvas = Config.Canvas

"""
Usage Cli <height> <width> <host> <port>

This file is a prototype with lots of poor choices(in my opinion)
It is just something that was hacked together. The rest of the code doesn't reflect this file
"""


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
            nspace = copy.copy(self.parameterDictContainer[0])
            nspace.pop('canvas')
            for word, val in nspace.items():
                if word[:n] == text:
                    matches.append(word)
            return matches
        else:
            for nspace in [self.namespace]:
                for word, val in nspace.items():
                    if word[:n] == text:
                        matches.append(self._arg_postfix(self._callable_postfix(val, word)))
            return matches

    
    def _callable_postfix(self, val, word):
        if hasattr(val, '__call__') and word in self.statePatternDict:
            word = word + "()"
        elif hasattr(val, '__call__') and word not in self.patternDict:
            word = word + "("
        return word
    def _arg_postfix(self, word):
        if word=='arg(':
            word = word + "' ')("
        return word
    
    def setPatternDict(self,pDict):
        self.patternDict=pDict
        
    def setStatePatternDict(self,spDict):
        self.statePatternDict=spDict
        
    def setParameterDictContainer(self,pDictContainer):
        self.parameterDictContainer=pDictContainer

def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

def safe_raw_input(message):
    #Removes leading whitespaces as well as any character that can't be printed with a standard american keyboard
    instruction = raw_input(message)
    cleanInstruction =  re.sub('[^a-zA-Z0-9-_*\ \\\/\'\"\!\@\#\$\%\^\&\*\_\-\+\=\.\,\?\[\]\{\}\|\~\`\;\:\(\).]', '', instruction.strip())
    return cleanInstruction

def runCliCurtain(argv):
    print 
    print "CLI to combine patterns"
    print "Press TAB for completion and suggestions"
    print "If running in Python press CTRL+A for all commands"
    print 'Write pattern code, parameter(r), recurrentParameter(rr), List (l), Save (s) or Safe Save (ss)'
    print 
    
    dictAll=UIUtils.getDictOfFunctions()
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
    completer.setStatePatternDict(StatePatterns.getStatePatternDic())

    try:
        readline.read_history_file('./.history')
    except:
        pass
    
    readline.set_completer(completer.complete)
    
    height, width, host, port = argv
    height = int(height)
    width = int(width)
    port = int(port)

    patternString = "random"

    patternContainer = [basicPattern.randomPattern]
    rContainer = [None]
    rrContainer = [None]
    resetFrameContainer = [False]
    patternInput = UIUtils.createInitialPatternInput(height, width)
    patternInputContainer=[patternInput]
    sendRate = Config.SendRate
    threadSender = UIUtils.startSendData(host = host,
                  port = port,
                  sendRate = sendRate,
                  patternContainer = patternContainer, #modified by the UI
                  rContainer = rContainer, #modified by the UI and sender
                  rrContainer = rrContainer, #modified by the UI and sender
                  patternInputContainer = patternInputContainer, #Should never be modified by the UI
                  resetFrameContainer= resetFrameContainer, #Should be set to 'true' every time 
                                        #a pattern is set even if it is the
                                        #same pattern
                  isClosed = lambda : False, #Modified by the UI
                  colorConverter = colorConverter, #Converts colors between colorspaces
                  canvasToData = P.canvasToData #Convers canvas to data
                  )

    completer.setParameterDictContainer(patternInputContainer)
    while(patternContainer[0]):
        try:
            instruction = safe_raw_input('Pattern code, parameter(r), recurrentParameter(rr), List (l), \nSave (s), Safe Save (ss), Save W/ args (srr), saveFunction (sf)\n')
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
                        rContainer[0]=command
                    elif len(instruction)>2 and instruction[0]=="r" and instruction[1]=='r' and instruction[2]==' ':
                        command = instruction[3:]
                        rrContainer[0]=command
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
                    elif instruction =="s" or instruction =="ss" \
                         or instruction == "srr":
                        name = safe_raw_input('Name for previous pattern:\n')
                        if name:
                            if instruction=="s":
                                exec UIUtils.savePattern(name,patternString) in globals(),locals()
                                globals()[name] = patternContainer[0]
                                dictAll[name]=globals()[name]
                                
                            elif instruction=="ss":
                                exec UIUtils.safeSavePattern(name,patternString) in globals(),locals()
                                globals()[name] = isolateCanvas(patternContainer[0])
                                dictAll[name]=globals()[name]
                                
                            elif instruction=="srr":
                                newPatternString = "arg('''"+\
                                                   rrContainer[0] +\
                                                   " ''')("+\
                                                   patternString+\
                                                   ")"
                                exec UIUtils.savePattern(name,newPatternString) in globals(),locals()
                                globals()[name] = eval(newPatternString)
                                dictAll[name]=globals()[name]
                    elif instruction =="sf":
                        func = safe_raw_input('Write Function. Use "pattern" as the input:\n')
                        leftP = func.count('(')
                        rightP = func.count(')')
                        if(leftP > rightP):
                            print "Attempting to fix mismatched left parenthesis"
                            func=func+ ')'*(leftP-rightP)
                        elif (rightP>leftP):
                            print "Attempting to fix mismatched right parenthesis"
                            func='('*(rightP-leftP) +func
                        name = safe_raw_input('Name for function:\n')
                        if name:
                            savedFunction = UIUtils.saveFunction(name,func, patternInputContainer[0])
                            if savedFunction:
                                dictAll[name]=globals()[name]=savedFunction
                    else:
                        function = eval(instruction)
                        patternString=instruction
                        patternContainer[0]=function
                        resetFrameContainer[0]=True

            except:
                traceback.print_exc(file=sys.stdout)


                
        except:
            patternContainer[0] = None
            print "threads successfully closed"


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



