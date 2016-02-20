# -*- coding: utf-8 -*-
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns
import Patterns.ExtraPatterns.StatePatterns as StatePatterns
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import SavedPatterns



def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

importFunctionsFromDict(Pattern.getPatternDic())
importFunctionsFromDict(Function.getFunctionDict())
importFunctionsFromDict(Function.getMetaFunctionDict())
importFunctionsFromDict(StatePatterns.getStatePatternDic())

@Function.function('__hueShift4Beat')
def __hueShift4Beat(pattern):  return arg('hue=totalBeats%4/4.')(hueShift(pattern))
@Function.function('__gameOfLiferizer')
def __gameOfLiferizer(pattern):  return step(pattern, gameOfLife(trivial))
@Function.function('__bluerizer')
def __bluerizer(pattern):  return arg('colorizeHue=0.7')(colorize(pattern))
@Function.function('__beatInt4Hue')
def __beatInt4Hue(pattern):  return arg('hue=int(totalBeats)/4. ')(hueShift(pattern))
