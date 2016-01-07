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


