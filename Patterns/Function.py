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
    def metaFunction(function):
        def functionOfPatterns(*patterns):
            def runOnceApplyDefaultArguments(patternInput):
                for key in kwargs.keys():
                    if not patternInput.has_key(key):
                        patternInput[key]=kwargs[key]
                    else:
                        pass
                return patternInput
            return compose(function(*patterns),runOnceApplyDefaultArguments)
        return functionOfPatterns
    return metaFunction

@function('defaultArgsP')
def defaultArgsP(**kwargs):
    '''
    usage: defaultArgs(arg=value)(function) -> function
    defaultArgs(arg=value)(function)(pattern) -> pattern
    order of execution: function(pattern(applyDefaultArguments))
    '''
    @rFunctionize
    def runOnceApplyDefaultArguments(patternInput):
        if any([not patternInput.has_key(key) for key in kwargs.keys()]):
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
        frame = patternInput['frame']
        if step[0]==False or frame==0:
            step[0]=True
            return pattern0(patternInput)
        else:
            return pattern1(patternInput)
    steppedPattern.__name__= "Stepped: " + str(pattern0.__name__) + "->"+str(pattern1.__name__)
    return steppedPattern

 

'''
End of meta functions
'''

#Isolate shouldn't change the parameters of the input, only the canvas??
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
        previousInput[0]=pattern(previousInput[0])
        canvas = copy.deepcopy(previousInput[0]['canvas'])
        patternInput['canvas']=canvas
        return patternInput
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

@function('colorize')
@defaultArguments(colorizeHue=1, colorizeAmount=0.5)
@functionize
def colorizeHue(patternInput):
    colorizeHue=patternInput["colorizeHue"]
    colorizeAmount=patternInput["colorizeAmount"]
    def colorizer(rgb,y,x):
        h,s,v = colorsys.rgb_to_hsv(*rgb)
        difference = colorizeHue-h
        if difference  > abs(colorizeHue-h-1):
            difference = (colorizeHue-h-1)%1
        h=colorizeAmount*difference + h
        return colorsys.hsv_to_rgb(h,s,v)
    canvas=patternInput["canvas"]
    canvas.mapFunction(colorizer)
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


def combineCanvas(colorCombiner):
    def combineFunction(*patterns):
        def combinedPattern(patternInput):
            patternOutputs=[]
            for pattern in patterns:
                patternOutputs.append(pattern(copy.deepcopy(patternInput)))
            canvass=[]
            for patternOutput in patternOutputs:
                canvass.append(patternOutput['canvas'])
            def combiner(rgb,y,x):
                return colorCombiner(*[canvas[y,x] for canvas in canvass])
            canvas=patternInput['canvas']

            for patternOutput in patternOutputs:
                patternInput.update(patternOutput)
                
            canvas.mapFunction(combiner)
            patternInput['canvas']=canvas
            return patternInput
        return combinedPattern
    return combineFunction


@function('meanP')
@combineCanvas
def meaner(*colors):
    colorOutput= tuple([sum(color)/len(colors) for color in zip(*colors)])
    return colorOutput

@function('addP')
@combineCanvas
def addPattern(*colors):
    colorOutput= tuple([sum(color) for color in zip(*colors)])
    return colorOutput


@function('weightedMean2P')
@defaultArguments(weightedMeanWeight=0.5)
def weightedMeanP(*patterns):
    def weighter(patternInput):
        weight=patternInput['weightedMeanWeight']
        @combineCanvas
        def meaner(color0, color1):
            colorOutput= tuple([color[0]*weight+color[1]*(1-weight) for color in zip(color0, color1)])
            return colorOutput
        return meaner(*patterns)(patternInput)
    return weighter





@function('mask')
@combineCanvas
def masker(color0, color1, color2):
    if any(color0):
        colorOutput= color1
    else:
        colorOutput=color2
    return colorOutput

@function('weightedMask')
@combineCanvas
def weightedMasker(color0, color1, color2):
    weight = color0[0]
    colorOutput=tuple([color[0]*weight+color[1]*(1-weight) for color in zip(color1, color2)])
    return colorOutput


import math
import collections

@function('arg')
def arg(strInstructionToEval):
    def updaterArg(pattern):
        def updateArg(patternInput):
            oldPatternInput = copy.copy(patternInput)
            oldPatternInput.pop('canvas')
            try:
                execInPattern(strInstructionToEval, patternInput)
                newPatternInput=pattern(patternInput)
            except:
                newPatternInput=pattern(patternInput)
                execInPattern(strInstructionToEval, newPatternInput)
                newPatternInput=pattern(newPatternInput)
            newPatternInput.update(oldPatternInput)
            return newPatternInput
        return updateArg
    return updaterArg

def getArgDicts(patternInput):
    return patternInput

def execInPattern(strInstructionToEval, patternInput):
    defaultDict =getEvalDefaultDict()
    exec strInstructionToEval in defaultDict, patternInput

def getEvalDefaultDict():
    defaultDict =collections.defaultdict(int)
    defaultDict['abs']=abs
    defaultDict['max']=max
    defaultDict['min']=min
    defaultDict['str']=str
    defaultDict['float']=float
    defaultDict['int']=int
    defaultDict['len']=len



    defaultDict.update(math.__dict__)
    return defaultDict

def hsvShifter(rgb,amount):
    h,s,v=colorsys.rgb_to_hsv(*rgb)
    h +=amount
    return colorsys.hsv_to_rgb(h,s,v)


@function('timeChangerArrays')
def timechange(patternnArray, timeArray):
    totalTime = sum(timeArray)
    startTime=getCurrentTime()

    def timeChangedPattern(patternInput):
        timeElapsed=(getCurrentTime()-startTime)
    
        timeElapsed%=totalTime

        for i in xrange(len(timeArray)):
            time=timeArray[i]
            if timeElapsed>time:
                timeElapsed = timeElapsed-time
            else:
                return patternnArray[i](patternInput)
        return lambda x: x #Should never happen
    return timeChangedPattern


@function('timeChanger')
@defaultArguments(timeChangerTime =6)
def timechanger(*patterns):
    startTime=getCurrentTime()
    lenPat = len(patterns)
    frameContainer=[0]
    previousIndexContainer=[0]
    numberOfCyclesContainer=[0]
    def timeChangedPattern(patternInput):
        timeTransition=patternInput["timeChangerTime"]
        timeElapsed=(getCurrentTime()-startTime)
        totalTime = lenPat*timeTransition
        numberOfCycles = int(timeElapsed/totalTime)
        if not numberOfCyclesContainer[0] == numberOfCycles:
            #If just completed a full cycle, reset frame
            #Useful if there is only one pattern in the timeChaner
            #And this pattern uses the frame count
            
            numberOfCyclesContainer[0]=numberOfCycles
            previousIndexContainer[0]=-1
            
        timeElapsed%=totalTime
        index = int(timeElapsed/timeTransition)

        if not previousIndexContainer[0] == index:
            patternInput["previousPattern"] = patterns[previousIndexContainer[0]]
            patternInput["previousFrame"] = frameContainer[0]
            previousIndexContainer[0]=index
            frameContainer[0]=0
        thisPatternInput = copy.copy(patternInput)
        thisPatternInput['frame']=frameContainer[0]
        frameContainer[0]+=1
        return patterns[index](thisPatternInput)
        
    return timeChangedPattern

import time
def getCurrentTime():
    return time.time()



@function('translate')
@defaultArguments(xTranslate=0, yTranslate=0)
@functionize
def translate(patternInput):
    '''
    percentage translator. args('xTranslate=0; yTranslate=0')
    '''
    height=patternInput["height"]
    width=patternInput["width"]
    xTranslate=patternInput["xTranslate"]
    yTranslate=patternInput["yTranslate"]

    xTranslate = round(xTranslate*width)
    yTranslate = round(yTranslate*height)
    oldcanvas = copy.deepcopy(patternInput["canvas"])

    def translator(rgb,y,x):
        positionY=int((y+yTranslate)%height)
        positionX=int((x+xTranslate)%width)
        color = oldcanvas[positionY, positionX]
        return color
    canvas=patternInput["canvas"]
    canvas.mapFunction(translator)
    patternInput['canvas']=canvas
    return patternInput



@function('blur')
@functionize
def blur(patternInput):
    '''
    blures image
    '''

    oldcanvas = copy.deepcopy(patternInput["canvas"])

    def blurer(rgb,y,x):
        color =tuple([sum(color)/9 for color in zip(*[oldcanvas[y+i,x+j] for i in [-1,0,1] for j in [-1,0,1]])])
        return color
    canvas=patternInput["canvas"]
    canvas.mapFunction(blurer)
    patternInput['canvas']=canvas
    return patternInput


@function('gameOfLife')
@defaultArguments(lifeSurviveRange=[2,3], lifeBornRange=[3], lifeOtherSurviveRatio=0.5, lifeNeighborDistance=1)
@functionize
def gameOfLife(patternInput):
    '''
    Games of life with colors
    #http://www.mirekw.com/ca/ca_gallery2.html#LIFE
    '''

    oldcanvas = copy.deepcopy(patternInput["canvas"])
    aliveRange = patternInput['lifeSurviveRange']
    deadRange = patternInput['lifeBornRange']
    otherColorRatio= patternInput['lifeOtherSurviveRatio']
    lifeNeighborDistance=patternInput['lifeNeighborDistance']
    neighborRange= range(-lifeNeighborDistance,lifeNeighborDistance+1)
    def isAlive(aliveMe, aliveN, aliveNOtherColor):
        keepAlive = (aliveMe and (aliveN+aliveNOtherColor*otherColorRatio in aliveRange))
        becomeAlive = not aliveMe and (aliveN in deadRange)
        return keepAlive or becomeAlive
    def gamerOfLife(rgb,y,x):
        aliveAll = [int(sum(map(lambda x: x>0.5,color))) for color in zip(*[oldcanvas[y+i,x+j] for i in neighborRange for j in neighborRange])]
        aliveMe = [color>0.5 for color in rgb]
        aliveNeighbor = [aliveAll[i]- aliveMe[i] for i in xrange(3)]
        aliveNAll = sum(aliveNeighbor)
        aliveNOtherColor = [aliveNAll - aliveNeighbor[i] for i in xrange(3)]
        color = tuple([ isAlive(aliveMe[i],aliveNeighbor[i], aliveNOtherColor[i]) for i in xrange(3)])
        return color
    canvas=patternInput["canvas"]
    canvas.mapFunction(gamerOfLife)
    patternInput['canvas']=canvas
    return patternInput


@function('gameOfGeneration')
@defaultArguments(generationSurviveRange=[3,4,5], generationBornRange=[2], generationStates=4, generationNeighborDistance=1)
@functionize
def gameOfGeneration(patternInput):
    '''
    Games of generation
    #http://www.mirekw.com/ca/ca_gallery2.html#LIFE
    '''

    oldcanvas = copy.deepcopy(patternInput["canvas"])
    surviveRange = patternInput['generationSurviveRange']
    bornRange = patternInput['generationBornRange']
    neighborDistance=patternInput['generationNeighborDistance']
    neighborRange= range(-neighborDistance,neighborDistance+1)
    numberOfStates = patternInput['generationStates']
    epsilon = 0.001
    states = [(0,0,0)]+[colorsys.hsv_to_rgb(float(h)/numberOfStates +epsilon,1,1) for h in xrange(numberOfStates)]
    # 0=dead, 1= new, >1 = decaying
    def getState(color):
        if not any ([channel>0.4 for channel in color]):
            return 0
        else:
            h,s,v = colorsys.rgb_to_hsv(*color)
            return (int(h*numberOfStates)%numberOfStates)+1

    #1= new, 2 = decaying
    def oldOrNew(newNeigh):
        if newNeigh in surviveRange:
            return 1
        else:
            return 2

    def gamerOfGeneration(rgb,y,x):
        stateMe = getState(rgb)
        if (stateMe>1): #decay
            newState = (stateMe+1)
        else:
            newAll = sum([getState(oldcanvas[y+i, x+j])==1 for i in neighborRange for j in neighborRange])
            newMe = int(stateMe==1)
            newNeigh = newAll-newMe

            if newMe:
                newState=oldOrNew(newNeigh)
            elif newNeigh in bornRange:
                newState=1
            else:
                newState=0

        newState = newState% (numberOfStates+1)            
        return states[newState]
    canvas=patternInput["canvas"]
    canvas.mapFunction(gamerOfGeneration)
    patternInput['canvas']=canvas
    return patternInput



@function("frameRate")
@defaultArguments(frameRate=30)
def frameRate(pattern):
    '''
    Changes the frame of the patternInput at the specified rate
    '''
    miliseconds=1000
    previousTimeContainer = [time.time()*miliseconds]
    previousFrameContainer = [0]
    def frameRated(patternInput):
        fRate=patternInput['frameRate']
        thisTime = time.time()*miliseconds
        newPatternInput = copy.copy(patternInput)
        previousFrameContainer[0]+= (thisTime - previousTimeContainer[0])/miliseconds*fRate
        newPatternInput['frame']=int(previousFrameContainer[0])
        previousTimeContainer[0]=thisTime
        return pattern(newPatternInput)
    return frameRated


#############
#Code that needs to be made more clear


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

@function("updateRate")
@defaultArguments(updateRate=30)
def timedPattern(pattern):
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
        rate=patternInput['updateRate']
        thisTime=time.time()*miliseconds
        if(PREVIOUS_TIME[0]!=None):
            frames = int((thisTime - PREVIOUS_TIME[0])/miliseconds*rate)
            if(frames>0):
                PREVIOUS_TIME[0]=thisTime
        else:
            frames=0
            PREVIOUS_TIME[0]=time.time()*miliseconds
        return frames
    return intCache(timeFrames)(pattern)


#End of code that needs to be made more clear
#############


####################
#Start of transitions, i.e. functions that use the previousPattern

import Config
import random
TransitionMask = Config.Canvas

def transitionAbstract(transitionFunction, init, isDone):
    def transitionPattern(pattern):
        doneContainer=[False]
        previousPatternContainer=[None]
        recursionLock = [0]
        transitionPatternContainer=[None]
        transitionDict={}
        def transitioner(patternInput):
            if recursionLock[0] >= 2:
                return pattern(patternInput)
            recursionLock[0]+=1
            frame =  patternInput['frame']
            if frame ==0 :
                doneContainer[0] = False
                previousPatternContainer[0]= None
                transitionPatternContainer[0]=None
                transitionDict.clear()
            done = doneContainer[0]
            if not done:
                transition = transitionPatternContainer[0]
                if transition == None:
                    transitionPatternContainer[0] = transitionFunction
                    transition = transitionPatternContainer[0]
                    init(transitionDict)
                if previousPatternContainer[0]==None:
                    previousPattern = isolate(patternInput['previousPattern'])
                    oldPatternInputInitializer = copy.copy(patternInput)
                    oldPatternInputInitializer['frame']=oldPatternInputInitializer['previousFrame']
                    try:
                        previousPattern(oldPatternInputInitializer)
                        previousPatternContainer[0]=previousPattern
                    except:
                        pass
                previousPattern = previousPatternContainer[0]
                if previousPattern:
                    if not isDone(transitionDict):
                        newPatternInput = transitionFunction(previousPattern, pattern, patternInput, transitionDict)
                    else:
                        done=True
                        doneContainer[0]=done
                        previousPatternContainer[0]=None
                        newPatternInput= pattern(patternInput)
                else:
                    done=True
                    doneContainer[0]=done
                    newPatternInput= pattern(patternInput)
            else:
                newPatternInput= pattern(patternInput)
            recursionLock[0]-=1
            return newPatternInput
        return transitioner
    return transitionPattern

def transitionFadeFunction(previousPattern, pattern, patternInput, transitionDict):
    transitionStep = patternInput['transitionFadeStep']
    if transitionDict['weight']==None:
        transitionDict['weight']= 0
    weight = transitionDict['weight']
    if weight <1:
        weight += transitionStep
        transitionDict['weight'] = weight
        oldWeight=None
        try:
            oldWeight = patternInput['weightedMeanWeight']
        except:
            pass
        patternInput['weightedMeanWeight']=weight
        newPatternInput = weightedMeanP(pattern, previousPattern)(patternInput)
        if oldWeight!=None:
            newPatternInput['weightedMeanWeight']=oldWeight
        else:
            newPatternInput.pop('weightedMeanWeight')
        newPatternInput= newPatternInput
    else:
        done=True
        doneContainer[0]=done
        previousPatternContainer[0]=None
        newPatternInput= pattern(patternInput)
    return newPatternInput

def transitionFadeInit(transitionDict):
    transitionDict['weight']=None

@function('transitionFade')
@defaultArguments(transitionFadeStep=0.005)
def transitionFade(pattern):
    return transitionAbstract(transitionFadeFunction, transitionFadeInit, lambda transitionDict: transitionDict['weight']>=1)(pattern)


def transitionRandomFunction(previousPattern, pattern, patternInput, transitionDict):
    height = patternInput['height']
    width = patternInput['width']
    transitionRandomPixels = patternInput['transitionRandomPixels']
    if transitionDict['transitionMask']==None:
        transitionDict['transitionMask']= TransitionMask(height=height, width=width)
    if transitionDict['randomGenerator']==None:
        heightR = range(height)
        widthR = range(width)
        coordinates= [(x,y) for y in heightR for x in widthR]
        random.shuffle(coordinates)
        generator = (x for x in coordinates)
        transitionDict['randomGenerator']=generator
    try:
        generator=transitionDict['randomGenerator']
        transitionMask=transitionDict['transitionMask']
        for i in xrange(transitionRandomPixels):
            x,y = generator.next()
            transitionMask[y,x] = (1,0,0)
        transitionInput = copy.copy(patternInput)
        transitionInput['canvas'] = transitionMask
        transitionPattern = lambda *args:transitionInput
        newPatternInput = masker(transitionPattern, pattern, previousPattern)(patternInput)
    except:
        transitionDict['done']=True
        newPatternInput = pattern(patternInput)
    return newPatternInput

def transitionRandomInit(transitionDict):
    transitionDict['transitionMask']=None
    transitionDict['randomGenerator']=None
    transitionDict['done']=False

@function('transitionRandom')
@defaultArguments(transitionRandomPixels=10)
def transitionRandom2(pattern):
    return transitionAbstract(transitionRandomFunction, transitionRandomInit, lambda transitionDict: transitionDict['done'])(pattern)
