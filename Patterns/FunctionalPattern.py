import time
from functools import wraps

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


def timedPattern(frameRate=30):
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
    def timeFrames(*args, **kwargs):
        thisTime=time.time()*miliseconds
        if(PREVIOUS_TIME[0]!=None):
            frames = int((thisTime - PREVIOUS_TIME[0])/miliseconds*frameRate)
            if(frames>0):
                PREVIOUS_TIME[0]=thisTime
        else:
            frames=0
            PREVIOUS_TIME[0]=time.time()*miliseconds
        return frames
    return lambda function:intCache(timeFrames)(function)


def framePattern(intFunction):
    '''
    Takes  a function to calculate the frame, 
    a frameGetter (a function that takes an int and returns
    a frame, and returns a pattern

    Example usage:
    @framePattern(lambda x:2*x)
    def frameGetter(x):
	return x

    frameGetter(2)->4
    '''
    def buildPatternFrame(frameGetter):
        @wraps(frameGetter)#preserves __name__ and __doc__
        def getFrame(*args, **kwargs):
            frame=intFunction(*args, **kwargs)
            return frameGetter(frame)
        return getFrame
    return buildPatternFrame

def timedFramePattern(frameRate=30):
    '''
    Takes a frame rate and a function that takes a frame;
    returns the result of the frameGetter for the particular frameRate
    in time

    Example:
    @timedFramePattern()
    def test(x):
	return x
    
    while(1):
	test(1)
    '''
    miliseconds=1000
    START_TIME = time.time()*miliseconds
    def timeFrames(*args, **kwargs):
        thisTime = time.time()*miliseconds
        return int((thisTime - START_TIME)/miliseconds*frameRate)
    return lambda frameGetter:framePattern(timeFrames)(frameGetter)

    
def buildStaticFramePattern(intFunction, frameGetter):
    def staticFramePattern(x):
        frame=intFunction(x)
        return frameGetter(frame)
    return staticFramePattern


def buildTimedFramePattern(frameGetter,frameRate=30):
    START_TIME = time.time()
    def getFrame(x):
        thisTime = time.time()
        frame = int((thisTime - START_TIME)*frameRate)
        return frame
    return buildStaticFramePattern(getFrame, frameGetter)


def buildStaticGeneratorPattern(intFunction, generatorBuilder, generatorParams):
    generator=generatorBuilder(generatorParams)
    cache=[generator.next()]
    def staticGeneratorPattern(x):
        numberOfUpdates=intFunction(x)
        for i in xrange(numberOfUpdates):
            cache[0]=generator.next()
        return cache[0]
    return staticGeneratorPattern



def buildTimedPurePattern(pattern,frameRate=30):
    PREVIOUS_TIME = [None] 
    cache=[None]
    def runPattern(x):
        thisTime = time.time()
        frame = int((thisTime - START_TIME)*frameRate)
    
def buildConditionalRunPattern(intFunction, pattern):
    cache=[None]
    def getPattern(x):
        if cache[0]:
            numberOfRuns=intFunction(x)
            for i in xrange(numberOfRuns):
                cache[0]=pattern(x)
        else:
            cache[0]=pattern(x)
        return cache[0]
    return getPattern(x)




