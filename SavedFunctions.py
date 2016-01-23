# -*- coding: utf-8 -*-
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image



def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

importFunctionsFromDict(Pattern.getPatternDic())
importFunctionsFromDict(Function.getFunctionDict())
importFunctionsFromDict(Function.getMetaFunctionDict())

@Function.function('__hueShift4Beat')
def __hueShift4Beat(pattern):  return arg('hue=totalBeats%4/4.')(hueShift(pattern))
@Function.function('__gameOfLiferizer')
def __gameOfLiferizer(pattern):  return step(pattern, gameOfLife(trivial))
@Function.function('__bluerizer')
def __bluerizer(pattern):  return arg('colorizeHue=0.7')(colorize(pattern))
