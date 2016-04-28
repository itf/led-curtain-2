import random
import math
import colorsys
import Patterns.Pattern as P
import Patterns.StaticPatterns.basicPatterns as BP

import Patterns.Function as F
import Patterns.ExtraPatterns.StatePatterns as SP


@P.pattern("testInput")
def testInput(patternInput):
    inputs = patternInput['input']
    if inputs.has_key('1') and inputs['1']=='a':
        return BP.redPattern(patternInput)
    else:
        return BP.greenPattern(patternInput)

###########
#Begin simple snake


UP=["KEY_UP","W","w"]
DOWN=["KEY_DOWN","S","s"]
RIGHT=["KEY_UP","D","d"]
LEFT=["KEY_RIGHT","A","a"]

def simpleSnakeInit(statePatternDict, patternInput):
    '''
    Initializes/restarts the dict for the fade transition
    '''
    
    statePatternDict['previousTotalBeats']=patternInput['totalBeats']
    
    statePatternDict['snakesBodies']={}
    

def simpleSnakePatternFunction(patternInput,statePatternDict):


    height =patternInput['height']
    width =patternInput['width']

    previousBeats=int(statePatternDict['previousTotalBeats'])
    thisBeats = int(patternInput['totalBeats'])
    inputs = patternInput['input']
    snakesBodies = statePatternDict['snakesBodies']

    deadSnakes=[]
    for sB in snakesBodies:
        if sB not in inputs:
                deadSnakes.append(sB)
    for i in deadSnakes:
        snakesBodies.pop(i)

    for sB in inputs:
        if sB not in snakesBodies:
            snakesBodies[sB]=[[random.randint(1,height), random.randint(1,width)]]

    if (thisBeats>previousBeats):
        statePatternDict['previousTotalBeats'] = thisBeats
        for snakeBody in snakesBodies:
            snakesBodies[snakeBody].append(snakeBody[-1])
            statePatternDict['snakesBodies']=snakesBodies

    deadSnakes=[]
    for sB in snakesBodies:
        snakeBody=snakesBodies[sB]
        snakeBodySize = len(snakeBody)
        for i in xrange(snakeBodySize-1,0,-1):
            snakeBody[i]=snakeBody[i-1]

        direction = inputs[sB]
        y,x = snakeBody[0]
        if direction in UP:
            head= [y-1,x]
        elif direction in DOWN:
           head = [y+1,x]
        elif direction in RIGHT:
            head= [y,x+1]
        else:
            head= [y,x-1]
        head[0]=head[0]%height
        head[1]=head[1]%width

        for sB2 in snakesBodies:
            snakeBody2=snakesBodies[sB2]
            if head in snakeBody2:
                deadSnakes.append(sB)
                break
                
        snakeBody[0]=head
    for deadSnake in deadSnakes:
        snakesBodies.pop(deadSnake)
    patternInput = BP.blackPattern(patternInput)
    canvas = patternInput['canvas']
    for sB in snakesBodies:
        snakeBody=snakesBodies[sB]
        for yx in snakeBody:
            y,x = yx
            canvas[y,x]=(1,0,0)
            
        y,x = snakeBody[0]
        canvas[y,x]=(0,0,1)
    
        
    return patternInput

def simpleSnakeIsDone(statePatternDict):

    return False

@SP.statePattern('simpleSnakeInput')
@SP.makeStatePattern(simpleSnakePatternFunction,simpleSnakeInit,simpleSnakeIsDone)
def simpleSnakePattern():
    '''
    A simple snake that turns and grows with the beat
    '''
    pass
