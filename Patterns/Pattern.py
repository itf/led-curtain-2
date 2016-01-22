'''
This file defines functions to be used for creating patterns, and
defines the PatternInput

Patterns are functions that take a PatternInput and return a PatternInput
The patternInput has a Canvas inside it and all the parameters related
to the pattern.

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
                 frame=0,
                 params=None,
                 canvas=None,
                 globalBrightness=0.1):
        self['width']=width
        self['height']=height
        self['frame']=frame
        self['params']=params
        self['canvas']=canvas
        self['globalBrightness']=globalBrightness
        
    def __getitem__(self, key):
        item = dict.__getitem__(self,key)
        if  hasattr(item, '__call__'):
            return item()
        else:
            return item
        
    def __deepcopy__(self,memo):
        #needed in order to copy the functions properly 
        newone = copy.copy(self)
        newone['canvas'] = copy.deepcopy(self['canvas'])
        return newone

