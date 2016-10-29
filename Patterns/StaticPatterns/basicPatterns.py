import random
import math
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
    '''
    (PatternInput) -> hue rainbow
    '''
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


@P.pattern('rgb')
@F.defaultArgsP(rgbR=1,
                rgbB = 0,
                rgbG=0,
                rgbEquation="",
                )
def rgbPattern(patternInput):
    '''
    Defines values or equations for rgbR, rgbB, rgbG.
    To set equations such as "cos(x)", use quotes for the value of rgb.
    '''
    equation= patternInput["rgbEquation"]
    height = float(patternInput["height"])
    width = float(patternInput["width"])
    getVal=patternInput.getValFunction()
    rgbR = patternInput["rgbR"]
    rgbB = patternInput["rgbB"]
    rgbG = patternInput["rgbG"]

    def mapper(rgb,y,x):
        if equation:
            xyDict={'x':x/width,'y':y/height}
            F.execInPattern(equation,patternInput,xyDict)
        r = getVal(rgbR,x,y, 'rgbR', rgb = rgb)
        b = getVal(rgbB,x,y, 'rgbB', rgb = rgb)
        g = getVal(rgbG,x,y, 'rgbG', rgb = rgb)
        return (r,g,b)
    canvas=patternInput["canvas"]
    canvas.mapFunction(mapper)
    return patternInput


@P.pattern('cubeHelix')
@F.defaultArgsP(cubeHelixAngle = 0,
                cubeHelixLight = 0.77,
                cubeHelixGamma = 1
                )
def cubeHelixPattern(patternInput):
    '''
    A tentative colorhelix color space. The colors look really pretty
    Use it to make a more friendly rainbow, to graph, etc.
    '''
    cubeHelixAngle = patternInput["cubeHelixAngle"]
    cubeHelixLight = patternInput["cubeHelixLight"]
    cubeHelixGamma = patternInput["cubeHelixGamma"]

    getVal=patternInput.getValFunction()
    def mapper(rgb,y,x):
        angle = float(getVal(cubeHelixAngle,x,y, 'cubeHelixAngle'))
        light = float(getVal(cubeHelixLight,x,y, 'cubeHelixLight'))
        gamma = float(getVal(cubeHelixGamma,x,y, 'cubeHelixGamma'))
        r, g, b =  _cubeHelix(angle, light, gamma)
        return (r,g,b)
    canvas=patternInput["canvas"]
    canvas.mapFunction(mapper)
    return patternInput

@F.simpleCached(1800)
def _cubeHelix(normalizedAngle, lightParameter = 0.77, gamma = 1):
    #####
    # Based on Dave Green's `cubehelix' colour scheme,
    # and jradavenport cubehelix python implementation
    # and ideas from A Less-Angry Rainbow by mike bostock
    #
    _rgbAngle= normalizedAngle*3.1416*2
    _rgbf= (-abs(0.5-(_rgbAngle/3.1416/2.+0.01)%1)**gamma)*1.05+lightParameter
    _rgbS=1.5+_rgbf*2.2
    _rgbAmp=_rgbS * _rgbf * (1. - _rgbf) / 2.
    rgbR=_rgbf+_rgbAmp*(-0.14861 * math.cos(_rgbAngle) + 1.78277 * math.sin(_rgbAngle))
    rgbG=_rgbf+_rgbAmp*(-0.29227 * math.cos(_rgbAngle) - 0.90649 * math.sin(_rgbAngle))
    rgbB=_rgbf+_rgbAmp * (1.97294 * math.cos(_rgbAngle))
    return (rgbR, rgbG, rgbB)



patternDefaultDict = F.getEvalDefaultDict()
equationPlane = []
rotatedPlane=[]
@P.pattern('equationxyPlotter')
@F.defaultArgsP(equationXY="sin(10*(x**2+y**2))/3.",
                equationXmin = -1,
                equationXmax = 1,
                equationYmin = -1,
                equationYmax = 1,
                equationAngle0 = 0
                )
def equation(PatternInput):
    '''
    Not well tested. Creates a 3d equation plot that can be rotated
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    iterations =1

    if equationPlane==[]:
        for i in xrange(height*iterations):
            equationPlane.append([0]*width*iterations)
    equation=PatternInput["equationXY"]
    equationXmin = PatternInput["equationXmin"]
    equationXmax = PatternInput["equationXmax"]
    equationYmin = PatternInput["equationYmin"]
    equationYmax = PatternInput["equationYmax"]
    equationAngle0 = PatternInput["equationAngle0"]
    angle=equationAngle0

    dx = float(equationXmax-equationXmin)/width
    dy = float(equationYmax-equationYmin)/height

    minZ= [+999999999]
    maxZ= [-999999999]
    @F.simpleCached(2)
    def calculateEquationPlane(equation):
        for y0 in xrange(height*iterations):
            y=y0-mHeight*iterations
            y = y*dy/iterations
            for x0 in xrange(width*iterations):
                x= x0-mWidth*iterations
                x = x*dx/iterations
                z =eval(equation, patternDefaultDict, locals())

                equationPlane[y0][x0]=z
                if minZ[0]>z:
                    minZ[0]=z
                if maxZ[0]<z:
                    maxZ[0]=z
        return equationPlane
    
    calculateEquationPlane(equation)

    maxZ=maxZ[0]
    minZ=minZ[0]
    dz = maxZ-minZ

    if rotatedPlane ==[]:
        for i in xrange(height):
            rotatedPlane.append([None]*width)
    else:
        for i in xrange(height):
            for j in xrange(width):
                rotatedPlane[i][j]=None


    def rotateEquation(angle,equationPlane):
        antiAngle= abs(1 - angle**2)**0.5
        for y in xrange(height*iterations):
            for x in xrange(width*iterations):
                z = equationPlane[y][x]
                y2 = int(round(y*(antiAngle)/iterations + (z/dy+mHeight) * angle))
                z2 = z*(antiAngle) - (y- mHeight)*dy * angle/iterations
                if y2<height and y2>=0:
                    if rotatedPlane[y2][x/iterations]==None:
                        rotatedPlane[y2][x/iterations] = z
                    elif rotatedPlane[y2][x/iterations]< z2:
                        rotatedPlane[y2][x/iterations]=z


    if angle!=0:
        rotateEquation(angle,equationPlane)
        plotPlane=rotatedPlane
    else:
        plotPlane=equationPlane
    def calculateEquation(eq,x,y):
        return eval(eq, patternDefaultDict, locals())
    def mapper(rgb,y,x):
        h=plotPlane[height-y-1][width-x-1]
        if h==None:
            h=0
            s=0
            v=0
        else:
            h=(h-minZ)/dz
            s=1
            v=h*0.5+0.5
        color =colorsys.hsv_to_rgb(h,s,v)
        return color
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper) 
    return PatternInput

@P.pattern('circle')
@F.defaultArgsP(circleRadius=0.666)
def circle(PatternInput):
    '''
    Creates a circle centered at the canvas
    With the radius normalized to the smalles dimension of the canvas
    default: circleRadius = "0.666"
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    circleRadius=PatternInput['circleRadius']
    getVal = PatternInput.getValFunction()
    def mapper(rgb,y,x):
        circleR = getVal(circleRadius, x, y)
        circleR = (circleR * min(mWidth, mHeight))
        sCRadius = circleR ** 2

        if (mWidth-x)**2 +(mHeight-y)**2 > sCRadius:
            return (0,0,0)
        else:
            return (1,0,0)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput



DEBUG_POLYGON=False
@P.pattern('polygon2')
@F.defaultArgsP(polygonRadius = 0.666,
                polygonSizes = 4)
def polygon(PatternInput):
    '''
    Creates a polygon centered at the canvas
    With the radius normalized to the smallest dimension of the canvas
    default: circleRadius = "0.666"
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth = width/2
    mHeight = height/2
    polygonRadius = PatternInput['polygonRadius']
    polygonRadius = (polygonRadius * min(mWidth, mHeight))
    polygonSizes = PatternInput['polygonSizes']

    @F.simpleCached(5000)
    def isInside(x, y, polygonRadius, polygonSizes):
        inside = 1
        xCoef = 0
        yCoef = 1
        angle = math.pi *2 / polygonSizes
        for i in range(int(math.ceil(polygonSizes))):
            distanceFromPlane = (x-mWidth) * xCoef + (y-mHeight) * yCoef
            if DEBUG_POLYGON:
                if abs(distanceFromPlane-polygonRadius)<0.5:
                    return 1.5
                    pass
            if distanceFromPlane > polygonRadius:
                inside *= max(0, polygonRadius+1-distanceFromPlane) #makes the edges not sharp
                if inside==0:
                    break
            xCoef, yCoef = xCoef*math.cos(angle) +  yCoef*math.sin(-angle), \
                            xCoef*math.sin(angle) +  yCoef*math.cos(angle)
        return inside

    def mapper(rgb, y, x):
        inside = isInside(x, y, polygonRadius, polygonSizes)
        return (inside,0,0)
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput

@P.pattern('polygon')
@F.defaultArgsP(polygonRadius = 0.666,
                polygonSizes = 4,
                polygonAlisasing = 1,
                polygonSparePlanes = 0)
def polygon3(patternInput):
    '''
    Creates a polygon centered at the canvas
    With the radius normalized to the smallest dimension of the canvas
    default: circleRadius = "0.666"
    '''
    width = patternInput["width"]
    height = patternInput["height"]
    mWidth = width/2
    mHeight = height/2
    polygonRadius = patternInput['polygonRadius']
    polygonRadius = (polygonRadius * min(mWidth, mHeight))
    polygonSizes = patternInput['polygonSizes']
    polygonAlisasing = patternInput['polygonAlisasing']
    polygonSparePlanes = patternInput['polygonSparePlanes']
    def isInside(x, y, polygonRadius, polygonSizes):
        inside = 1
        outsidePlanes = polygonSparePlanes+1
        angle = math.pi *2 / polygonSizes
        nextVertexX = -math.sin(angle/2)*polygonRadius
        nextVertexY = math.cos(angle/2)*polygonRadius
        negativeAngle = (math.ceil(polygonSizes)*angle-angle/2)
        vertexX = -math.sin(negativeAngle)*polygonRadius
        vertexY = math.cos(negativeAngle)*polygonRadius
        planes = 0
        for i in range(int(math.ceil(polygonSizes))):
            xCoef =  nextVertexY- vertexY
            yCoef = vertexX- nextVertexX
            epsilon=1e-10
            xCoef,yCoef = xCoef/math.sqrt(xCoef**2+yCoef**2+epsilon), yCoef/math.sqrt(xCoef**2+yCoef**2+epsilon)
            vertexDistance = xCoef*nextVertexX + yCoef* nextVertexY
            distanceFromPlane = (x-mWidth) * xCoef + (y-mHeight) * yCoef
            if DEBUG_POLYGON:
                if x == int(mWidth+vertexX) and y == int(mHeight+vertexY):
                    return 2
                    pass
                if abs(distanceFromPlane-vertexDistance)<0.5:
                    return 1.5
                    pass
            if distanceFromPlane > vertexDistance:
                inside *= min(1,max(0, vertexDistance+polygonAlisasing-distanceFromPlane)) #makes the edges not sharp
                outsidePlanes -=1
                inside = max(inside,min(1,outsidePlanes))
            vertexX, vertexY = nextVertexX, nextVertexY
            nextVertexX, nextVertexY = vertexX * math.cos(angle) + vertexY * math.sin(-angle), \
                                       vertexX * math.sin(+angle) + vertexY * math.cos(angle)

        return inside

    def mapper(rgb, y, x):
        inside = isInside(x, y, polygonRadius, polygonSizes)
        return (inside,0,0)
    canvas=patternInput["canvas"]
    canvas.mapFunction(mapper)
    return patternInput


@P.pattern('radialHueGradient')
@F.defaultArgsP(radialGradientRadius=0.666,
                radialGradientColor0 = 0x6495ed,
                radialGradientColor1=0x0ffff,
                radialGradientPos=0)
def radialHueGradient(PatternInput):
    '''
    Radial Hue gradient.
    Depends on radialGradientRadius,
                radialGradientColor0,
                radialGradientColor1,
                radialGradientPos
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    circleRadius=PatternInput['radialGradientRadius']
    circleRadius = (circleRadius * min(mWidth, mHeight))
    epsilon=0.001
    circleRadius=max(circleRadius,epsilon)
    sCRadius=circleRadius**2

    gradientColor0 = PatternInput["radialGradientColor0"]
    gradientColor1 = PatternInput["radialGradientColor1"]
    gradientPos = PatternInput["radialGradientPos"]

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
        normalizedRadius = (float(radius)/circleRadius +gradientPos) %1
        h,s,v = h0+dh*normalizedRadius , s0+ds*normalizedRadius, v0+dv*normalizedRadius
        return colorsys.hsv_to_rgb(h,s,v)
        
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput


@P.pattern('linearHueGradient')
@F.defaultArgsP(linearGradientLength=1,
                linearGradientColor0 = 0x6495ed,
                linearGradientColor1=0x00f08,
                linearGradientPos=0.5,
                linearGradientAngle=0)
def linearHueGradient(PatternInput):
    '''
    Linear Gradient.
    Depends on:
        linearGradientLength,
        linearGradientColor0,
        linearGradientColor1,
        linearGradientPos,
        linearGradientAngle
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    mWidth=width/2
    mHeight=height/2
    length=PatternInput['linearGradientLength']
    length = round(length * max(width, height))
    epsilon=0.001
    length=max(length,epsilon)

    gradientColor0 = PatternInput["linearGradientColor0"]
    gradientColor1 = PatternInput["linearGradientColor1"]
    gradientPos = PatternInput["linearGradientPos"]

    rg0,b0= divmod(gradientColor0, 0x100)
    r0,g0 = divmod(rg0, 0x100)

    rg1,b1= divmod(gradientColor1, 0x100)
    r1,g1 = divmod(rg1, 0x100)

    r0,g0,b0 = r0/255.,g0/255.,b0/255.
    r1,g1,b1 = r1/255.,g1/255.,b1/255.
    
    h0,s0,v0 = colorsys.rgb_to_hsv(r0,g0,b0)
    h1,s1,v1 =  colorsys.rgb_to_hsv(r1,g1,b1)

    dh, ds, dv = h1-h0, s1-s0, v1-v0

    linearGradientAngle=PatternInput["linearGradientAngle"]
    pi=3.1415926

    angle=linearGradientAngle*pi*2

    x=math.cos(angle)
    y=math.sin(angle)

    dist = lambda X,Y: (X*x+Y*y)
    
    def mapper(rgb,y,x):
        x=x-mWidth
        y=y-mHeight
        distance = dist(x,y)
        normalizedDistance = (float(distance)/length +gradientPos) %1
        h,s,v = h0+dh*normalizedDistance , s0+ds*normalizedDistance, v0+dv*normalizedDistance
        return colorsys.hsv_to_rgb(h,s,v)
        
    canvas=PatternInput["canvas"]
    canvas.mapFunction(mapper)
    return PatternInput



patternDefaultDict = F.getEvalDefaultDict()
@P.pattern('equationxPlotter')
@F.defaultArgsP(equationX="sin(x*3)/3",
                equationXxmin = -3,
                equationXxmax = 3,
                )
def equationX(PatternInput):
    '''
    2 dimensional equation plotter
    Example: equationX="sin(x*3)/3"
    '''
    width = PatternInput["width"]
    height = PatternInput["height"]
    equation=PatternInput["equationX"]
    equationXmin = PatternInput["equationXxmin"]
    equationXmax = PatternInput["equationXxmax"]

    dx=float(equationXmax-equationXmin)/width
    
    mWidth=width/2
    mHeight=height/2

    blackPattern(PatternInput)
    
    canvas=PatternInput["canvas"]
    
    for xi in xrange(width):
        x=(xi-1/2.)*dx+equationXmin
        y0 =eval(equation, patternDefaultDict, locals())
        x=x+dx
        y1 =eval(equation, patternDefaultDict, locals())

        if y0<y1:
            y0,y1=y1,y0
        y0,y1 = int(round(mHeight*(1-y0))), int(round(mHeight*(1-y1)))
        for yi in xrange(y0,y1+1):
            canvas[yi,xi]=(1,0,0)
    return PatternInput
