import random
import colorsys
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
@F.defaultArgsP(cRadius=0.666)
def circle(PatternInput):
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    cRadius=PatternInput['cRadius']
    cRadius = round(cRadius * min(mWidth, mHeight))
    sCRadius=cRadius**2
    def mapper(rgb,y,x):
        if (mWidth-x)**2 +(mHeight-y)**2 > sCRadius:
            return (0,0,0)
        else:
            return (1,0,0)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput

@P.pattern('radialHueGradient')
@F.defaultArgsP(gradientRadius=0.666, gradientColor0 = 0x6495ed, gradientColor1=0x0ffff, gradientPos=0)
def radialHueGradient(PatternInput):
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    cRadius=PatternInput['gradientRadius']
    cRadius = round(cRadius * min(mWidth, mHeight))
    sCRadius=cRadius**2

    gradientColor0 = PatternInput["gradientColor0"]
    gradientColor1 = PatternInput["gradientColor1"]
    gradientPos = PatternInput["gradientPos"]

    rg0,b0= divmod(gradientColor0, 0x100)
    r0,g0 = divmod(rg0, 0x100)

    rg1,b1= divmod(gradientColor1, 0x100)
    r1,g1 = divmod(rg1, 0x100)

    r0,g0,b0 = r0/255.,g0/255.,b0/255.
    r1,g1,b1 = r1/255.,g1/255.,b1/255.
    
    h0,s0,v0 = colorsys.rgb_to_hsv(r0,g0,b0)
    h1,s1,v1 =  colorsys.rgb_to_hsv(r1,g1,b1)

    dh, ds, dv = h1-h0, s1-s0, v1-v0
    
    def mapper(rgb,y,x):
        radius = ((mWidth-x)**2 +(mHeight-y)**2)**0.5
        normalizedRadius = (float(radius)/cRadius +gradientPos) %1
        h,s,v = h0+dh*normalizedRadius , s0+ds*normalizedRadius, v0+dv*normalizedRadius
        return colorsys.hsv_to_rgb(h,s,v)
        
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput
