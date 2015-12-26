def compose(f,g):
    return lambda x: f(g(x))

def timechange(functionArray, timeArray, startTime):
    totalTime = sum(timeArray)
    timeElapsed=(startTime-getCurrentTime)
    
    while(timeElapsed>totalTime):
        timeElapse-=totalTime

    for(i in xrange(len(timeArray))):
        if timeElapsed>time:
            timeElapsed = timeElapsed-time
        else:
            return functionArray(i)
    else:
        return lambda x: x #Should never happen
        

def getCurrentTime():
    raise Exception("Not Implemented")
