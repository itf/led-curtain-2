import random
import ScreenCanvas
import Patterns.Pattern as P

@P.pattern("random")
@P.canvasPattern
def randomPattern(PatternInput):
    height = PatternInput['height']
    width = PatternInput['width']
    canvas=ScreenCanvas.Canvas(height=height, width=width)
    canvas.mapFunction(_getRandomColor)
    return canvas

def _getRandomColor(value, y, x):
    return (random.random(),random.random(),random.random())

@P.pattern("trivial")
def trivialPattern(PatternInput):
    return PatternInput

@P.pattern("red")
def randomPattern(PatternInput):
    canvas=PatternInput['canvas']
    canvas.mapFunction(_getRedColor)
    return PatternInput

def _getRedColor(value, y, x):
    return (1,0,0)
