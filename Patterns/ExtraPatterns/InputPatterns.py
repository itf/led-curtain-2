import random
import math
import colorsys
import Patterns.Pattern as P
import Patterns.StaticPatterns.basicPatterns as BP

import Patterns.Function as F
import Patterns.ExtraPatterns.StatePatterns as SP


@P.pattern("testInput")
def testInput(patternInput):
    inputs = patternInput['lastInput']
    if inputs.has_key('1') and inputs['1']=='a':
        return BP.redPattern(patternInput)
    else:
        return BP.greenPattern(patternInput)

###########
#Begin simple snake


UP=["KEY_UP","W","w"]
DOWN=["KEY_DOWN","S","s"]
RIGHT=["KEY_RIGHT","D","d"]
LEFT=["KEY_LEFT","A","a"]

def simpleSnakeInit(statePatternDict, patternInput):
    '''
    Initializes/restarts the dict for the fade transition
    '''
    
    statePatternDict['previousTotalBeats']=patternInput['totalBeats']
    
    statePatternDict['snakesBodies']={}
    statePatternDict['snakesColors']={}
    
    

def simpleSnakePatternFunction(patternInput,statePatternDict):


    height =patternInput['height']
    width =patternInput['width']

    previousBeats=int(statePatternDict['previousTotalBeats'])
    thisBeats = int(patternInput['totalBeats'])
    inputs = patternInput['lastInput']
    snakesBodies = statePatternDict['snakesBodies']
    snakesColors = statePatternDict['snakesColors']

    deadSnakes=[]
    for sB in snakesBodies:
        if sB not in inputs:
                deadSnakes.append(sB)
    for i in deadSnakes:
        snakesBodies.pop(i)
        snakesColors.pop(i)

    for sB in inputs:
        if sB not in snakesBodies:
            snakesBodies[sB]=[[random.randint(1,height), random.randint(1,width)]]
            snakesColors[sB]= [random.random(),random.random(),random.random()]

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
            canvas[y,x]=snakesColors[sB]
            
        y,x = snakeBody[0]
        r,g,b = snakesColors[sB]
        canvas[y,x]=(1-r,1-g,1-b)
    
        
    return patternInput

def simpleSnakeIsDone(statePatternDict):

    return False

@SP.statePattern('simpleSnakeGame')
@SP.makeStatePattern(simpleSnakePatternFunction,simpleSnakeInit,simpleSnakeIsDone)
def simpleSnakePattern():
    '''
    A simple snake that turns and grows with the beat controlled by the user
    '''
    pass


####
#Agario clone



def agarioInit(statePatternDict, patternInput):
    '''
    Initializes/restarts the dict for the fade transition
    '''
    height = patternInput['height']
    width = patternInput['width']

    x = random.randint(0,width-1)
    y = random.randint(0,height-1)
    statePatternDict['food']=[[y,x]]
    statePatternDict['foodColor'] = [0,1,0]


    x = random.randint(0,width-1)
    y = random.randint(0,height-1)
    statePatternDict['poison']=[[y,x]]
    statePatternDict['poisonColor'] = [1,0,0]

    
    statePatternDict['blobBodies']={}
    statePatternDict['blobSpeeds']={}
    statePatternDict['blobMovements']={}
    statePatternDict['blobColors']={}

    statePatternDict['maxSpeed'] = 1
    statePatternDict['speedStep'] = 0.1
    
    

def agarioPatternFunction(patternInput,statePatternDict):


    height =patternInput['height']
    width =patternInput['width']

    inputs = patternInput['inputList']
    blobBodies = statePatternDict['blobBodies']
    blobColors = statePatternDict['blobColors']
    blobSpeeds = statePatternDict['blobSpeeds']
    blobMovements = statePatternDict['blobMovements']
    maxSpeed = statePatternDict['maxSpeed'] = 1
    speedStep = statePatternDict['speedStep'] = 0.1
    
    poisons=statePatternDict['poison']
    poisonColor=statePatternDict['poisonColor']

    foods =  statePatternDict['food']
    foodColor = statePatternDict['foodColor']

    ##Remove expired playes
    deadBlobs=[]
    for sB in blobBodies:
        if sB not in inputs:
                deadBlobs.append(sB)
    for i in deadBlobs:
        blobBodies.pop(i)
        blobColors.pop(i)
        blobSpeeds.pop(i)
        blobMovements.pop(i)

    ##Add new players or dead players back
    for sB in inputs:
        if sB not in blobBodies:
            x = random.randint(1,width)
            y = random.randint(1,height)
            blobBodies[sB] = [[y,x],[y, x-1],[y-1, x],[y, x+1],[y+1, x]]
            blobColors[sB]= [random.random(),random.random(),random.random()]
            blobSpeeds[sB] = [0,0]
            blobMovements[sB] = [0,0]

    ##Move Poison:
    for poison in poisons:
        poisonMovement = random.randint(1,5)
        if poisonMovement == 2:
            poison[0]+=1
        elif poisonMovement == 3:
            poison[0]-=1
        elif poisonMovement == 4:
            poison[1]+=1
        elif poisonMovement == 5:
            poison[1]-=1
        poison[0]%=height
        poison[1]%=width

    deadBlobs=[]
    growBlob={}
    for bb in blobBodies:
        growBlob[bb]=0
        blobBody=blobBodies[bb]
        blobBodySize = len(blobBody) 
        directionList = inputs[bb]

        ##Change speed
        if directionList:
            direction=directionList.pop(0)
            y,x = blobSpeeds[bb]
            if direction in UP:
                blobSpeeds[bb]= [y-speedStep,x]
            elif direction in DOWN:
                blobSpeeds[bb] = [y+speedStep,x]
            elif direction in RIGHT:
                blobSpeeds[bb]= [y,x+speedStep]
            elif direction in LEFT:
                blobSpeeds[bb]= [y,x-speedStep]
                
            blobSpeeds[bb][0]= min(max(-maxSpeed,blobSpeeds[bb][0]),maxSpeed)
            blobSpeeds[bb][1]=min(max(-maxSpeed,blobSpeeds[bb][1]),maxSpeed)

        blobMovements[bb][0]+=blobSpeeds[bb][0]
        blobMovements[bb][1]+=blobSpeeds[bb][1]

        #Move blob 
        dx = int(blobMovements[bb][1])
        dy = int (blobMovements[bb][0])
        blobMovements[bb][0]-=dy
        blobMovements[bb][1]-=dx
        
        for i in xrange(blobBodySize):
            blobBody[i][0]=(blobBody[i][0]+dy)%height
            blobBody[i][1]=(blobBody[i][1]+dx)%width

        ##Eat poison
        for i in xrange(blobBodySize):
            bodyPart = blobBody[i]
            if bodyPart in poisons:
                deadBlobs.append(bb)
                break
                
        ##Eat food
        for i in xrange(blobBodySize):
            bodyPart = blobBody[i]
            if bodyPart in foods:
                growBlob[bb]+=1
                foods.remove(bodyPart)
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)
                foods.append([y,x])

        ##Eat blobs o.O
        for otherBB in blobBodies:
            if otherBB != bb:
                blobHeart = blobBodies[otherBB][0]                 
                if blobHeart in blobBody:
                    growBlob[bb]+= len(blobBodies[otherBB])/2
                    deadBlobs.append(otherBB)
                        

    ##Make things grow:
        for bb in growBlob:
            size = growBlob[bb]
            blobBody=blobBodies[bb]

            for i in xrange(size):
                direction = random.randint(1,4)
                #Grow in random direction. Try 500 times
                sizeBody = len(blobBody)
                for i in xrange(500):
                    randomBodyPartN = random.randint(0,sizeBody-1)
                    randomBodyPart = blobBody[randomBodyPartN]
                    y,x = randomBodyPart
                    if direction == 1:
                        x+=1
                        x%=width
                    elif direction == 2:
                        x-=1
                        x%=width
                    elif direction == 3:
                        y+=1
                        y%=height
                    elif direction == 4:
                        y-=1
                        y%=height                        
                    newPart = [y,x]
                    if newPart not in blobBody:
                       blobBody.append(newPart)
                       break
                    
                
##        for sB2 in snakesBodies:
##            snakeBody2=snakesBodies[sB2]
##            if head in snakeBody2:
##                deadSnakes.append(sB)
##                break
##                
##        snakeBody[0]=head


    ##Kill blobs
    for deadBlob in deadBlobs:
        blobBodies.pop(deadBlob)


    patternInput = BP.blackPattern(patternInput)
    canvas = patternInput['canvas']

    #Draw the blobs
    for bb in blobBodies:
        blobBody=blobBodies[bb]
        for yx in blobBody:
            y,x = yx
            canvas[y,x]=blobColors[bb]
            
        y,x = blobBody[0]
        r,g,b = blobColors[sB]
        canvas[y,x]=(1-r,1-g,1-b)

    #Draw the poison
    for poison in poisons:
        y,x=poison
        canvas[y,x]=poisonColor
        
    #Draw the food
    for food in foods:
        y,x=food
        canvas[y,x]=foodColor

        
        
    return patternInput

def agarioIsDone(statePatternDict):

    return False

@SP.statePattern('agarioGame')
@SP.makeStatePattern(agarioPatternFunction,agarioInit,agarioIsDone)
def agarPattern():
    '''
    A simple agario copy game where a red dot kills you
    '''
    pass

