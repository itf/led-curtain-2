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
