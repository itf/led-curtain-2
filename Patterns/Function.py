'''
Functions are functions used to modify patterns. They take a pattern or multiple
patterns and output a different pattern.

Patterns functions that take a PatternInput and return a PatternInput 
'''
import colorsys
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
def compose(f,g):
    return lambda x: f(g(x))




'''
Fancier functions from here.
'''

@function('movingHue')
def movingHue(PatternInput):
    hueFrameRate=0.01
    width=PatternInput["width"]
    xHueShift =1./width
    if PatternInput.has_key("hueFrameRate"):
        hueFrameRate=PatternInput["hueFrameRate"]
    def shifter(rgb,y,x):
        amount=PatternInput["frame"]*hueFrameRate + xHueShift*x
        return hsvShifter(rgb,amount)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(shifter)
    return PatternInput
        
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
