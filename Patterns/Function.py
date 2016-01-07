'''
Functions are functions used to modify patterns. They take a pattern or multiple
patterns, besides arguments,  and output a different pattern.

Metafunctions take a function, and output a different function

Patterns are functions that take a PatternInput and return a PatternInput 
'''
import colorsys
import functools
from functools import wraps
import copy

_dict_of_functions={}
_dict_of_meta_functions={}
def function(name):
    '''
    To add your function to the dictionary of functions
    add the decorator @function(name) on your pattern.
    '''
    def builder(patternFunction):
        _dict_of_functions[name]=patternFunction
        return patternFunction
    return builder

def metaFunction(name):
    '''
    To add your metaFunction to the dictionary of metaFunctions
    add the decorator @metaFunction(name) on your pattern.
    '''
    def builder(metaFunction):
        _dict_of_meta_functions[name]=metaFunction
        return metaFunction
    return builder

def getFunctionDict():
    return _dict_of_functions

def getMetaFunctionDict():
    return _dict_of_meta_functions

@metaFunction("compose")
def compose(*functions):
    '''
    Composes one or more functions
    '''
    if len(functions)==1:
        return functions[0]
    elif len(functions)==2:
        return lambda patternInput: functions[0](functions[1](patternInput))
    else:
        nHalfFunctions = len(functions)/2
        return lambda patternInput: compose(*functions[0:nHalfFunctions])(compose(*functions[nHalfFunctions:])(patternInput))


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

def metaFunctionize(myMetaFunction):
    '''
    Takes a function that takes a pattern and returns a pattern
    and returns a metaFunction that takes a function and returns a function
    '''
    @wraps(myMetaFunction) #preserves __name__ and __doc__
    def metaFunction(function):
        return compose(myMetaFunction,function)
    return metaFunction

def rMetaFunctionize(myMetaFunction):
    '''
    Takes a function that takes a pattern and returns a pattern
    and returns a metaFunction that takes a function and returns a function
    See rFunctionize
    '''
    @wraps(myMetaFunction) #preserves __name__ and __doc__
    def metaFunction(function):
        return compose(function,myMetaFunction)
    return metaFunction

@metaFunction('defaultArgs')
def defaultArguments(**kwargs):
    '''
    usage: defaultArgs(arg=value)(function) -> function
    defaultArgs(arg=value)(function)(pattern) -> pattern
    order of execution: function(pattern(applyDefaultArguments))
    '''
    hasRun=[False]

    @rMetaFunctionize
    @rFunctionize
    def runOnceApplyDefaultArguments(patternInput):
        if hasRun[0]==False or any([not patternInput.has_key(key) for key in kwargs.keys()]):
            hasRun[0]=True
            patternInput.update(kwargs)
            return patternInput
        else:
            return patternInput
    return runOnceApplyDefaultArguments

@metaFunction('constArgs')
def constantArguments(**kwargs):
    '''
    usage: constantArgs(arg=value)(function) -> function
    constantArgs(arg=value)(function)(pattern) -> pattern
    order of execution: function(pattern(applyArguments))
    '''
    @rMetaFunctionize
    @functionize
    def applyArguments(patternInput):
        newPatternInput=copy.copy(patternInput)
        newPatternInput.update(kwargs)
        return newPatternInput
    return applyArguments

            
@function('constant')
def constant(pattern):
    '''
    Gets the output canvas once, always send the same output canvas
    '''
    cache = [None]
    @wraps(pattern) #preserves __name__ and __doc__
    def cached_f(patternInput):
        if cache[0]==None:
            cache[0] = copy.deepcopy(pattern(patternInput)['canvas'])
        patternInput['canvas']=copy.deepcopy(cache[0])
        return patternInput
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
End of meta functions
'''

@function('isolate')
def isolate(pattern):
    '''
    Runs the pattern in its own environment
    It updates the frame in each update
    '''
    previousInput = [None]
    @wraps(pattern) #preserves __name__ and __doc__
    def isolated(patternInput):
        if previousInput[0]==None:
            previousInput[0] = copy.deepcopy(patternInput)
        else:
            previousInput[0]['frame']+=1
        return copy.deepcopy(pattern(previousInput[0]))
    return isolated

@function('isolateCanvas')
def isolateCanvas(pattern):
    '''
    Runs the pattern in its own canvas environment
    '''
    previousCanvas = [None]
    @wraps(pattern) #preserves __name__ and __doc__
    def isolated(patternInput):
        if previousCanvas[0]==None:
            previousCanvas[0] = copy.deepcopy(patternInput['canvas'])
        isolatedPatternInput = copy.copy(patternInput)
        isolatedPatternInput['canvas']=previousCanvas[0]
        patternOutput = pattern(isolatedPatternInput)
        previousCanvas[0]=copy.deepcopy(patternOutput['canvas'])
        return patternOutput
    return isolated


@function('movingHue')
@defaultArguments(hueFrameRate=0.01)
@functionize
def movingHue(patternInput):
    hueFrameRate=patternInput["hueFrameRate"]
    def shifter(rgb,y,x):
        amount=patternInput["frame"]*hueFrameRate
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('hueShift')
@defaultArguments(hue=0.01)
@functionize
def movingHue(patternInput):
    hue=patternInput["hue"]
    def shifter(rgb,y,x):
        amount=hue
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('rainbownize')
@defaultArguments(nRainbows=1)
@functionize
def rainbownize(patternInput):
    numberOfRainbows=patternInput["nRainbows"]
    width=patternInput["width"]
    xHueShift =1./width
    def shifter(rgb,y,x):
        amount=xHueShift*x*numberOfRainbows
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('vRainbownize')
@defaultArguments(nVRainbows=1)
@functionize
def vRainbownize(patternInput):
    '''
    Vertical rainbownize
    '''
    numberOfRainbows=patternInput["nVRainbows"]
    height=patternInput["height"]
    yHueShift =1./height
    def shifter(rgb,y,x):
        amount=yHueShift*y*numberOfRainbows
        return hsvShifter(rgb,amount)
    canvas=patternInput["canvas"]
    canvas.mapFunction(shifter)
    return patternInput

@function('meanP')
def meanPattern(pattern0, pattern1):
    def meanP(patternInput):
        patternOutput0 = pattern0(copy.deepcopy(patternInput))
        patternOutput1 = pattern1(copy.deepcopy(patternInput))
        canvas0=patternOutput0['canvas']
        canvas1=patternOutput1['canvas']
        def meaner(rgb,y,x):
            return tuple([sum(color)/2 for color in zip(canvas0[y,x], canvas1[y,x])])
        canvas=patternInput['canvas']
        canvas.mapFunction(meaner)
        return patternInput
    return meanP
    
    

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
            return functionArray[i]
    else:
        return lambda x: x #Should never happen

        

def getCurrentTime():
    raise Exception("Not Implemented")

