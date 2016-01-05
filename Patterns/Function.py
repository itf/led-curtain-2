'''
Functions are functions used to modify patterns. They take a pattern or multiple
patterns, besides arguments,  and output a different pattern.

Or, they take a function, and output a different function

Patterns are functions that take a PatternInput and return a PatternInput 
'''
import colorsys
import functools
from functools import wraps

_dict_of_functions={}
def function(name):
    '''
    To add your function to the dictionary of functions
    add the decorator @function(name) on your pattern.
    '''
    def builder(patternFunction):
        _dict_of_functions[name]=patternFunction
        return patternFunction
    return builder

def getFunctionDict():
    return _dict_of_functions


@function("compose")
def compose(*functions):
    '''
    Composes one or more functions
    '''
    if len(functions)==1:
        return functions[0]
    elif len(functions)==2:
        return lambda x: functions[0](functions[1](x))
    else:
        return compose(functions[0],compose(*functions[1:]))


@function('constant')
def constant(pattern):
    '''
    Gets the output once, always send the same output
    '''
    cache = [None]
    @wraps(pattern) #preserves __name__ and __doc__
    def cached_f(patternInput):
        if cache[0]==None:
            cache[0] = pattern(patternInput)
        return copy.deepcopy(cache[0])
    return cached_f


@function('step')
def step(pattern0, pattern1):
    '''
    On first run it runs pattern0. On every
    following run it runs pattern1
    '''
    step = [False]
    def steppedPattern(patternInput):
        if step[0]==False:
            step[0]=True
            return pattern0(patternInput)
        else:
            return pattern1(patternInput)
    steppedPattern.__name__= "Stepped: " + str(pattern0.__name__) + "->"+str(pattern1.__name__)
    return steppedPattern

'''
Fancier functions from here.
'''

def functionize(myFunction):
    '''
    Turns a function that takes a patternInput and returns a patternInput
    into a function that takes a pattern and returns a pattern with
    its patternInput modified
    '''
    @wraps(myFunction) #preserves __name__ and __doc__
    def function(pattern):
        return compose(myFunction,pattern)
    return function

def rFunctionize(myFunction):
    '''
    Turns a function that takes a patternInput and returns a patternInput
    into a function that takes a pattern and runs the pattern on the modified
    patternInput
    '''
    @wraps(myFunction) #preserves __name__ and __doc__
    def function(pattern):
        return compose(pattern,myFunction)
    return function    

@function('movingHue')
@functionize
def movingHue(patternInput):
    hueFrameRate=0.01
    if patternInput.has_key("hueFrameRate"):
        hueFrameRate=patternInput["hueFrameRate"]
    def shifter(rgb,y,x):
        amount=patternInput["frame"]*hueFrameRate
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('rainbownize')
@functionize
def rainbownize(patternInput,numberOfRainbows=1):
    width=patternInput["width"]
    xHueShift =1./width
    def shifter(rgb,y,x):
        amount=xHueShift*x*numberOfRainbows
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('vRainbownize')
@functionize
def vRainbownize(patternInput, numberOfRainbows=1):
    '''
    Vertical rainbownize
    '''
    height=patternInput["height"]
    yHueShift =1./height
    def shifter(rgb,y,x):
        amount=yHueShift*y*numberOfRainbows
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput
        
def hsvShifter(rgb,amount):
    h,s,v=colorsys.rgb_to_hsv(*rgb)
    h +=amount
    return colorsys.hsv_to_rgb(h,s,v)

def timechange(functionArray, timeArray, startTime):
    totalTime = sum(timeArray)
    timeElapsed=(startTime-getCurrentTime)
    
    while(timeElapsed>totalTime):
        timeElapse-=totalTime

    for i in xrange(len(timeArray)):
        if timeElapsed>time:
            timeElapsed = timeElapsed-time
        else:
            return functionArray(i)
    else:
        return lambda x: x #Should never happen
        

def getCurrentTime():
    raise Exception("Not Implemented")
