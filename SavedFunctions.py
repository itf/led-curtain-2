# -*- coding: utf-8 -*-
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns
import Patterns.ExtraPatterns.StatePatterns as StatePatterns
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import Patterns.ExtraPatterns.HuslColor
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
@Function.function('__rotate')
def __rotate(pattern):  return defaultArgsP(rotateAngle=0, rotatex0=0.5, rotatey0=0.5)(arg('translateY="sin(rotateAngle)*(x-rotatex0)+cos(rotateAngle)*(y-rotatey0)-y-rotatey0"; translateX="cos(rotateAngle)*(x-rotatex0)-sin(rotateAngle)*(y-rotatey0)-x-rotatex0"')(translate(pattern)))
@Function.function('__wave')
def __wave(pattern):  return defaultArgsP(waveSlantY=0.5, waveYTransvAmp=0.2, waveYTransvPhase=0, waveYTransvFreq=0.5, waveYLongAmp=0, waveYLongFreq=1, waveYLongPhase=0, waveYPos=0, waveSlantX=-0.5, waveXTransvAmp=0.2, waveXTransvPhase=0, waveXTransvFreq=0.5, waveXLongAmp=0, waveXLongFreq=1, waveXLongPhase=0, waveXPos=0)(arg('translateY="x*waveSlantY+waveYTransvAmp*sin((x*waveYTransvFreq+waveYTransvPhase)*2*pi) +waveYLongAmp*sin((y*waveYLongFreq+waveYLongPhase)*2*pi) + waveYPos";translateX="y*waveSlantX+waveXTransvAmp*sin((y*waveXTransvFreq+waveXTransvPhase)*2*pi) +waveXLongAmp*sin((x*waveXLongFreq+waveXLongPhase)*2*pi) + waveXPos"')(translate(pattern)))
@Function.function('__beatDiamond')
def __beatDiamond(pattern):  return defaultArgsP(beatDiamondsNumber=3)(arg('hue="abs(int(max(abs(x+y-1),abs(x-y))-(totalBeats) ))/float(beatDiamondsNumber)"')(hueShift(pattern)))
