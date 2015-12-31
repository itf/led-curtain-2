import random
import ScreenCanvas
import Patterns.Pattern as P

@P.staticPattern
def randomPattern(PatternInput):
    height = PatternInput['height']
    width = PatternInput['width']
    canvas=ScreenCanvas.Canvas(height=height, width=width)
    canvas.mapFunction(getRandomColor)
    return canvas

def getRandomColor(value, y, x):
    return (random.random(),random.random(),random.random())
