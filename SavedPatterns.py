import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns


def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

importFunctionsFromDict(Pattern.getPatternDic())
importFunctionsFromDict(Function.getFunctionDict())
importFunctionsFromDict(Function.getMetaFunctionDict())

rotatingRainbow=Pattern.pattern('rotatingRainbow')(isolateCanvas(step(rainbow,vRainbownize(trivial))))

coolRandom=Pattern.pattern('coolRandom')(movingHue(constant(random)))

movingColors=Pattern.pattern('movingColors')(movingHue(red))
prettyDiagonalRainbow=Pattern.pattern('prettyDiagonalRainbow')(defaultArgs(hueFrameRate=0.02, nVRainbows=3, nRainbows=2)(compose(movingHue,vRainbownize,rainbownize))(red))

softRainbow=Pattern.pattern('softRainbow')(movingHue(meanP(movingColors,rainbow)))

rainbowAurora = Pattern.pattern('rainbowAurora')(isolateCanvas(movingHue(meanP(step(softRainbow,vRainbownize(trivial)),softRainbow))))

_pulsatingCircle = Pattern.pattern('_pulsatingCircle')(arg('cRadius=abs(frame%20-10)')(circle))

_explosionRed = Pattern.pattern('_explosionRed')(arg('cRadius = sin(frame/30.)*20; hue=0.05')(mask(circle,hueShift(trivial),meanP(red,trivial))))
meteorRainbow = Pattern.pattern('meteorRainbow')(arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2 ')(mask(translate(circle),meanP(softRainbow,trivial),blur(trivial))))
_mesmerezingMeteor = Pattern.pattern('_mesmerezingMeteor')(isolateCanvas(hueShift((arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2; weightedMeanWeight=0.03; hue=0.021')(mask(translate(circle),prettyDiagonalRainbow, weightedMean2P(black,blur(trivial))))))))

cloudsRainbow = Pattern.pattern('cloudsRainbow')(arg('generationBornRange=[3,4]; generationSurviveRange=[1,2,3]; generationStates=48; generationNeighborDistance=1 ')(isolate(step(circle,gameOfGeneration(trivial)))))