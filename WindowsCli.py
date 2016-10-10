#!/usr/bin/env python
#######################
# This files is intended to be used ONLY IN WINDOWS
# It is a hacked wrapper around the autocomplete of Cli.py.
#
# It is not possible to run readline inside pypy from windows, so the program does not have auto complete
# This files solves this problem by allowing to pipe the output onto the real program
# This files runs under cpython and pipes onto the main program that is running pypy
#
# How to use:
#
# From the command line, run:
#
# ./WindowsCli.py
#
# This file runs a mock version of the senders code, and runs the pattern and pattern input
#
#
from __future__ import print_function
import sys
import copy
import rlcompleter
import readline

try:
    import LocalConfig as Config
except:
    import Config
if Config.useAudio:
    import Audio.AudioClientLib as Audio

if Config.useInput:
    import Input.InputServerLib as Input

if Config.useOpenWeather:
    import UI.Weather as Weather

import UI.UIUtils as UIUtils
import Patterns.StaticPatterns.basicPatterns as basicPattern
import Patterns.Pattern as Pattern
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import Patterns.ExtraPatterns.StatePatterns as StatePatterns

import Patterns.ExtraPatterns.InputPatterns as InputPatterns
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import SavedPatterns
import SavedFunctions

import sys

import sys
import subprocess

class Completer(rlcompleter.Completer):
    '''
    Modifies rlcompleter.Completer to implement autocompletion
    '''

    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
        pos = readline.get_begidx()
        line = readline.get_line_buffer()
        nQuotes = line[0:pos].count("'")
        isR = len(line) > 1 and line[0] == 'r' and (
            line[1] == ' ' or (len(line) > 2 and line[1] == 'r' and line[2] == ' '))
        matches = []
        n = len(text)
        if (nQuotes % 2 == 1 or isR):
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
        if word == 'arg(':
            word = word + "' ')("
        return word

    def setPatternDict(self, pDict):
        self.patternDict = pDict

    def setStatePatternDict(self, spDict):
        self.statePatternDict = spDict

    def setParameterDictContainer(self, pDictContainer):
        self.parameterDictContainer = pDictContainer


def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]


def initializePatternInputParameters(patternInput):
    if Config.useAudio:
        patternInput["beat"] = 1
        patternInput["totalBeats"] = 1
        patternInput["bpm"] = 1

        patternInput["audioIntensity"] = 1
        patternInput["audioLowIntensity"] = 1

    if Config.useInput:
        patternInput["lastInput"] = 1
        patternInput["inputList"] = 1

    patternInput["time"] = 1
    patternInput["date"] = 1

    if Config.useOpenWeather:
        patternInput["temp"] = 1
        patternInput["tempF"] = 1
        patternInput["tempMax"] = 1
        patternInput["tempMin"] = 1
        patternInput["weather"] = 1
    patternInput["frame"] = 1


def runCliCurtain():
    try:
        cli = subprocess.Popen([Config.pypyPath, 'Cli.py'],
                           stdin=subprocess.PIPE)
    except:
        print("the path to pypy is wrong.")
        print("the path selected is" + Config.pypyPath)
        exit()

    def eprint(x):
        cli.stdin.write(x + "\n")

    dictAll = UIUtils.getDictOfFunctions()
    importFunctionsFromDict(dictAll)

    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind('"\C-r": reverse-search-history')
    readline.parse_and_bind('"\C-a" complete')
    readline.parse_and_bind('set menu-complete-display-prefix on')
    readline.parse_and_bind('set skip-completed-text on')
    readline.parse_and_bind('set completion-ignore-case on')
    readline.parse_and_bind('set blink-matching-paren on')
    completer = Completer(dictAll)
    completer.setPatternDict(Pattern.getPatternDic())
    completer.setStatePatternDict(StatePatterns.getStatePatternDic())

    try:
        readline.read_history_file('./.history')
    except:
        pass

    readline.set_completer(completer.complete)

    height = 1
    width = 1

    pattern = basicPattern.blackPattern
    patternInput = UIUtils.createInitialPatternInput(height, width)
    initializePatternInputParameters(patternInput)
    patternInputContainer = [patternInput]

    completer.setParameterDictContainer(patternInputContainer)
    while (pattern):
        try:
            instruction = raw_input('')
            print(instruction)
            readline.write_history_file('./.history')
            try:
                if instruction:
                    leftP = instruction.count('(')
                    rightP = instruction.count(')')
                    if (leftP > rightP):
                        instruction = instruction + ')' * (leftP - rightP)
                    elif (rightP > leftP):
                        instruction = '(' * (rightP - leftP) + instruction

                    if len(instruction) > 1 and instruction[0] == "r" and instruction[1] == ' ':
                        eprint(instruction)
                        command = instruction[2:]
                        try:
                            Function.execInPattern(command, patternInput)
                        except:
                            pass
                    elif len(instruction) > 2 and instruction[0] == "r" and instruction[1] == 'r' and instruction[
                        2] == ' ':
                        eprint(instruction)
                        command = instruction[3:]
                        try:
                            Function.execInPattern(command, patternInput)
                        except:
                            pass
                    elif instruction == "l":
                        eprint('l')
                    elif instruction == "s" or instruction == "ss" \
                            or instruction == "srr":
                        eprint(instruction)
                        name = raw_input('')
                        eprint(name)
                        if name:
                            dictAll[name] = basicPattern.trivialPattern  # assigns dummy pattern to save pattern
                    elif instruction == "sf":
                        func = raw_input('')
                        eprint(func)
                        name = raw_input('')
                        eprint(name)
                        if name:
                            savedFunction = UIUtils.saveFunction(name, func, patternInputContainer[0])
                            if savedFunction:
                                dictAll[name] = lambda x: x
                    else:
                        eprint(instruction)
                        function = eval(instruction)
                        patternString = instruction
                        pattern = function
                        try:
                            patternInput = pattern(patternInput)
                        except:
                            pass
            except:
                pass

        except:
            cli.communicate()
            exit()


def main(argv):
    runCliCurtain()


if __name__ == "__main__":
    main(sys.argv[1:])