import random
import math
import colorsys
import Patterns.Pattern as P
import Patterns.StaticPatterns.basicPatterns as BP

import Patterns.Function as F

'''
State Patterns are patterns that have an internal state
'''

import Config
import random
import copy
StateCanvas = Config.Canvas

_dict_of_state_patterns={}

def getStatePatternDic():
    return _dict_of_state_patterns

def statePattern(name):
    '''
    To add your pattern to the dictionary of patterns
    add the decorator @pattern(name) on your pattern.
    '''
    def builder(patternFunction):
        _dict_of_state_patterns[name]=patternFunction
        return patternFunction
    return builder

def makeStatePattern(*args):
    '''
    Takes a  patternFunction, init, isDone and returns a decorator
    that creates a pattern.
    See simpleSnakePattern
    '''
    patternFunction, init, isDone= args
    pattern = statePatternAbstract(patternFunction, init, isDone)
    def substitutePattern(patternPlaceHolder):
        pattern.__doc__ = patternPlaceHolder.__doc__
        pattern.__name__ = patternPlaceHolder.__name__
        def runPatternOrConstructor(*patternInput):
            if len(patternInput)==0: #Run constructor!
                return statePatternAbstract(patternFunction, init, isDone)
            else: #Run already constructed pattern
                return pattern(patternInput[0])
        return runPatternOrConstructor
    return substitutePattern
    

def statePatternAbstract(patternFunction, init, isDone):
    '''
    Helper function to create statePatterns.
    A a statePattern is defined by 3 things:
    1- a patternFunction, i.e. a function that takes:
        (patternInput, statePatternDict)

        It modifies statePatternDict as desired to keep its own state,
        and uses it and the patternInput to return a new pattern input.
        The statePatternDict is a dict used for the pattern to save its state.

    2- A init function, i.e. a function that takes
        (transitionDict, patternInput)
        The init function is the function responsible for initializing/restarting the statePatternDict
        So that the patternFunction has a working statePatternDict that it can use/ so that
        the patternDunction can be restarted.

    3- A IsDone function, i.e. a function that takes
        (statePatternDict)
        And decides if the pattern should be restarted
    '''

    doneContainer=[False]
    statePatternContainer=[None]
    statePatternDict={}
    def statePattern(patternInput):
        frame =  patternInput['frame']
        #Resets the pattern when the frame==0
        done = doneContainer[0]
        #Resets the pattern when the frame==0 or done
        if frame ==0 or done:
            doneContainer[0] = False
            statePatternContainer[0]=None
            statePatternDict.clear()
            
        pattern = statePatternContainer[0]
        if (pattern == None): #This means that the pattern has just initialized or has just restarted
            statePatternContainer[0]=patternFunction
            pattern = statePatternContainer[0]
            init(statePatternDict,patternInput)
        newPatternInput = pattern(patternInput,statePatternDict)
        done = isDone(statePatternDict)
        doneContainer[0]=done
        return newPatternInput
    return statePattern
            
###########
#Begin simple snake

def simpleSnakeInit(statePatternDict, patternInput):
    '''
    Initializes/restarts the dict for the fade transition
    '''
    
    statePatternDict['previousTotalBeats']=patternInput['totalBeats']
    
    statePatternDict['snakeBody']=[[0,0]]

    statePatternDict['snakeMax']=patternInput['width'] * patternInput['height'] / 8.

    statePatternDict['direction'] =0
    

def simpleSnakePatternFunction(patternInput,statePatternDict):
    UP=0
    DOWN=3
    RIGHT=1
    LEFT=2

    height =patternInput['height']
    width =patternInput['width']

    previousBeats=int(statePatternDict['previousTotalBeats'])
    thisBeats = int(patternInput['totalBeats'])
    snakeBody = statePatternDict['snakeBody']
    if (thisBeats>previousBeats):
        statePatternDict['previousTotalBeats'] = thisBeats
        direction = statePatternDict['direction']
        newDirection = random.randint(1,3)
        newDirection=((3-direction)+newDirection)%4
        statePatternDict['direction'] = newDirection
        snakeBody.append(snakeBody[-1])
        statePatternDict['snakeBody']=snakeBody

    direction = statePatternDict['direction']
    snakeBodySize = len(snakeBody)
    for i in xrange(snakeBodySize-1,0,-1):
        snakeBody[i]=snakeBody[i-1]


    y,x = snakeBody[0]
    if direction==UP:
        head= [y-1,x]
    if direction==DOWN:
       head = [y+1,x]
    if direction==RIGHT:
        head= [y,x+1]
    if direction==LEFT:
        head= [y,x-1]
    head[0]=head[0]%height
    head[1]=head[1]%width
    
    if head not in snakeBody:
        snakeBody[0]=head
    else:
        statePatternDict['direction'] = (direction+1)%4
    patternInput = BP.blackPattern(patternInput)
    canvas = patternInput['canvas']
    for yx in snakeBody:
        y,x = yx
        canvas[y,x]=(1,0,0)
        
    y,x = snakeBody[0]
    canvas[y,x]=(0,0,1)
    
        
    return patternInput

def simpleSnakeIsDone(statePatternDict):
    snakeBody=statePatternDict['snakeBody']
    done = (len(snakeBody) > statePatternDict['snakeMax'])
    return done

@statePattern('simpleSnake')
@makeStatePattern(simpleSnakePatternFunction,simpleSnakeInit,simpleSnakeIsDone)
def simpleSnakePattern():
    '''
    A simple snake that turns and grows with the beat
    '''
    pass
