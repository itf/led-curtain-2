import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns
import Patterns.ExtraPatterns.SimpleText


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

_pulsatingCircle = Pattern.pattern('_pulsatingCircle')(arg('cRadius=abs(frame%20-10)/10.')(circle))

_explosionRed = Pattern.pattern('_explosionRed')(arg('cRadius = sin(frame/30.)*4./3.; hue=0.05')(mask(circle,hueShift(trivial),meanP(red,trivial))))
meteorRainbow = Pattern.pattern('meteorRainbow')(arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2 ')(mask(translate(circle),meanP(softRainbow,trivial),blur(trivial))))
_mesmerezingMeteor = Pattern.pattern('_mesmerezingMeteor')(isolateCanvas(hueShift((arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2; weightedMeanWeight=0.05; hue=0.021')(mask(translate(circle),prettyDiagonalRainbow, weightedMean2P(black,blur(trivial))))))))

cloudsRainbow = Pattern.pattern('cloudsRainbow')(arg('generationBornRange=[3,4]; generationSurviveRange=[1,2,3]; generationStates=48; generationNeighborDistance=1 ')(isolate(step(circle,gameOfGeneration(trivial)))))

spaaceMoving = Pattern.pattern('spaaceMoving')(arg('textHeight=0.2; textPos=0.5; xTranslate= frame%17/17.; yTranslate=frame%33/33.; weightedMeanWeight=0 if frame%10==0 else 1')(step(black,mask(isolateCanvas(step(black,weightedMean2P(trivial,translate(text)))),softRainbow,arg('weightedMeanWeight=0.1 ')(weightedMean2P(black,blur(trivial)))))))
