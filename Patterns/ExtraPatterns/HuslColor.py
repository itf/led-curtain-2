import copy
import Patterns.Pattern as P
import Patterns.StaticPatterns.basicPatterns as basicPattern

import Patterns.Function as F
import Config
try:
    import LocalConfig as Config
except:
    pass
if Config.useHusl:
    import husl
    @F.simpleCached(1000)
    def huslShifter(rgb,dh, ds, dl):
        h,s,l=husl.rgb_to_husl(*rgb)
        h +=dh*360
        s +=ds*100
        l +=dl*100
        
        return husl.husl_to_rgb(h,s,l)

    @F.function('husl')
    @F.defaultArguments(huslH=0.01, huslS=0.01, huslL=0.01, huslEquation="")
    @F.functionize
    def huslShift(patternInput):
        '''
        Shifts the hue by the specified amount
        '''
        huslEquation=patternInput["huslEquation"]
        height = float(patternInput["height"])
        width = float(patternInput["width"])
        def shifter(rgb,y,x):
            if huslEquation:
                xyDict={'x':x/width,'y':y/height}
                F.execInPattern(huslEquation,patternInput,xyDict)
            huslH=patternInput["huslH"]
            huslS=patternInput["huslS"]
            huslL=patternInput["huslL"]
            return huslShifter(rgb,huslH,huslS,huslL)
        canvas=patternInput["canvas"]
        canvas.mapFunction(shifter)
        return patternInput
else:
    F.function('husl')(basicPattern.trivialPattern)
