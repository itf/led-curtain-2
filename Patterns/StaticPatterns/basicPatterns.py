import random
import ScreenCanvas
import Patterns.Pattern as P
import Patterns.Function as F


@P.pattern("random")
def randomPattern(PatternInput):
    '''
    (PatternInput) -> randomColors
    '''
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getRandomColor)
    return PatternInput

def _getRandomColor(value, y, x):
    return (random.random(),random.random(),random.random())

@P.pattern("trivial")
def trivialPattern(PatternInput):
    '''
    (PatternInput) -> (PatternInput)
    '''
    return PatternInput

@P.pattern("red")
def redPattern(PatternInput):
    '''
    (PatternInput) -> redCanvas
    '''
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getRedColor)
    return PatternInput

def _getRedColor(value, y, x):
    return (1,0,0)

@P.pattern("blue")
def bluePattern(PatternInput):
    '''
    (PatternInput) -> blueCanvas
    '''
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getBlueColor)
    return PatternInput

def _getBlueColor(value, y, x):
    return (0,0,1)

@P.pattern("green")
def greenPattern(PatternInput):
    '''
    (PatternInput) -> greenCanvas
    '''
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getGreenColor)
    return PatternInput

def _getGreenColor(value, y, x):
    return (0,1,0)

@P.pattern("black")
def blackPattern(PatternInput):
    '''
    (PatternInput) -> blackCanvas
    '''
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getBlackColor)
    return PatternInput

def _getBlackColor(value, y, x):
    return (0,0,0)

@P.pattern('rainbow')
def rainbow(PatternInput):
    width=PatternInput["width"]
    xHueShift =1./width
    def shifter(rgb,y,x):
        red=(1,0,0)
        amount=xHueShift*x
        return F.hsvShifter(red,amount)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(shifter)
    return PatternInput

@P.pattern('fractal')
@F.constant
def fractal(PatternInput):
    width=PatternInput["width"]
    xHueShift =1./width
    def mapper(rgb,y,x):
        intensity=(x**y%255)/255.
        color=(intensity,intensity,intensity)
        return color
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput


@P.pattern('circle')
@F.defaultArgsP(cRadius=10)
def circle(PatternInput):
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    cRadius=PatternInput['cRadius']
    sCRadius=cRadius**2
    def mapper(rgb,y,x):
        if (mWidth-x)**2 +(mHeight-y)**2 > sCRadius:
            return (0,0,0)
        else:
            return (1,0,0)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput
