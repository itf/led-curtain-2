'''
This file defines functions to be used for creating patterns, and
defines the PatternInput

Patterns are functions that take a PatternInput and return a PatternInput
The patternInput has a Canvas inside it.

'''

import time
import Patterns.Function as F
from functools import wraps
import copy

_dict_of_patterns={}
def getPattern(name):
    return _dict_of_patterns[name]

def getPatternDic():
    return _dict_of_patterns

def pattern(name):
    '''
    To add your pattern to the dictionary of patterns
    add the decorator @pattern(name) on your pattern.
    '''
    def builder(patternFunction):
        _dict_of_patterns[name]=patternFunction
        return patternFunction
    return builder



def canvasPattern(pattern):
    '''
    Since for most patterns it makes no sense to return the whole PatternInput,
but rather only the canvas, use the @canvasPattern decorator to turn a function
that returns a canvas into a pattern.
    '''
    @wraps(pattern) #preserves __name__ and __doc__
    def builder(patternInput):
        canvas = pattern(patternInput)
        patternInput['canvas']=canvas
        return patternInput
    return builder


def intCache(intFunctionCondition):
    '''
    Takes a function that returns an int or boolean, and then a function
    to be cached and returns the cached function
    The cached function when called will evaluate the intFunction->N and then
    run the function N times (in case it has side effects),
    and return the result.
    If N <1, it will return the previous result and not run the function
    again.

    Example usage:
    @intCache(lambda x: x>1)
    def test(x):
			return x
      
    prints the previous value of x if x<=1

    '''
    def buildFunctionWithIntCache(function):
        cache=[None]
        @wraps(function) #preserves __name__ and __doc__
        def cachedFunction(*args, **kwargs):
            if cache[0]!=None:
                numberOfRuns=intFunctionCondition(*args, **kwargs)
                for i in xrange(numberOfRuns):
                    cache[0]=function(*args, **kwargs)
            else:
                cache[0]=function(*args, **kwargs)
            return cache[0]
        return cachedFunction
    return buildFunctionWithIntCache

@F.function("updateRate")
def timedPattern(frameRate=30):
    '''
    Caches the output and updates it with the specified frameRate
    timedPattern(frameRate)(pattern)->pattern
    '''

    '''
    Returns a pattern that will only be called on the determined frameRate
    Example usage:

    @timedPattern(30)
    def test(x):
	return x

    for i in xrange(1000):
	test(i)

    Will print 0 untill 1/30 of a second has passed
    and then will print the value of i right after 1/30 of a second.
    '''
    PREVIOUS_TIME = [None]
    miliseconds=1000
    def timeFrames(patternInput):
        rate=frameRate
        if patternInput.has_key('frameRate'):
            rate=patternInput['frameRate']
        thisTime=time.time()*miliseconds
        if(PREVIOUS_TIME[0]!=None):
            frames = int((thisTime - PREVIOUS_TIME[0])/miliseconds*rate)
            if(frames>0):
                PREVIOUS_TIME[0]=thisTime
        else:
            frames=0
            PREVIOUS_TIME[0]=time.time()*miliseconds
        return frames
    return lambda function:intCache(timeFrames)(function)


@F.function("frameRate")
def frameRate(rate=30):
    '''
    Changes the frame of the patternInput at the specified rate
    '''
    miliseconds=1000
    START_TIME = time.time()*miliseconds
    @F.rFunctionize
    def frameRated(patternInput):
        fRate=rate
        if patternInput.has_key('frameRate'):
            fRate=patternInput['frameRate']
        thisTime = time.time()*miliseconds
        patternInput['frame']= int((thisTime - START_TIME)/miliseconds*fRate)
        return patternInput
    return frameRated

def framePattern(intFunction = lambda patternInput:patternInput["frame"]):
    '''
    Takes  a function to calculate the frame, 
    a frameGetter (a function that takes an int(frame Number) and returns
    a canvas, and returns a pattern

    Example usage:
    @framePattern(lambda x:2*x)
    def frameGetter(x):
	return x

    frameGetter(2)->4
    '''
    def buildPatternFrame(frameGetter):
        @wraps(frameGetter)#preserves __name__ and __doc__
        @canvasPattern
        def getFrame(patternInput):
            frame=intFunction(patternInput)
            return frameGetter(frame)
        return getFrame
    return buildPatternFrame

def timedFramePattern(frameRate=30):
    '''
    Takes a frame rate and a function that takes a frame;
    returns the result of the frameGetter for the particular frameRate
    in time.
    The frameRate can be overriden by the patternInput

    Example:
    @timedFramePattern()
    def test(x):
    return x
    
    while(1):
	test(1)
    '''
    miliseconds=1000
    START_TIME = time.time()*miliseconds
    def timeFrames(patternInput):
        rate=frameRate
        if patternInput.has_key('frameRate'):
            rate=patternInput['frameRate']
        thisTime = time.time()*miliseconds
        return int((thisTime - START_TIME)/miliseconds*rate)
    return lambda frameGetter:framePattern(timeFrames)(frameGetter)



'''
A pattern is a function that takes a PatternInput and returns a patternInput
'''

class PatternInput(dict):
    def __init__(self,
                 height,
                 width,
                 audioData=None,
                 frame=0,
                 params=None,
                 canvas=None):
        self['width']=width
        self['height']=height
        self['audioData']=audioData
        self['frame']=frame
        self['params']=params
        self['canvas']=canvas
    def __getitem__(self, key):
            return dict.__getitem__(self,key)
