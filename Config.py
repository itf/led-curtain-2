curtain = ""
useImages = False
useAudio = True
useInput = False
useHusl = False
useOpenWeather = False

class openWeather:
    api=""
    cityID="4931972"

import ScreenCanvasArray 
Canvas = ScreenCanvasArray.Canvas

if curtain=="old":
    width = 15
    height = 5
    host='10.0.63.101'
    port=6038
    import Transportation.Protocol.OldProtocol as P
    Protocol = P
    class ColorManagerConfig:
        ####
        #Sets gamma to BaseGamma + brightness * factor
        #This happens to improve the image quality, but it is not supported
        #by theory.
        redBaseGamma = 1.65
        greenBaseGamma = 1.55
        blueBaseGamma = 1.65
        redBrightnessFactor = 1.1
        greenBrightnessFactor = 1.2
        blueBrightnessFactor = 1.1
    import ColorManager as C
    convertColor = C.convertColorToLin #Converts the color profile to linear

elif curtain=='local': #Assume local
    width = 60
    height = 30
    host='localhost'
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
    class ColorManagerConfig:
        ####
        #Sets gamma to BaseGamma + brightness * factor
        #This happens to improve the image quality, but it is not supported
        #by theory.
        redBaseGamma = 2.4
        greenBaseGamma = 2.4
        blueBaseGamma = 2.4
        redBrightnessFactor = 0
        greenBrightnessFactor = 0
        blueBrightnessFactor = 0
    import ColorManager as C
    convertColor = C.convertColorToLin  #Converts the color profile to linear

elif curtain=='new': #New LED panel
    width = 60
    height = 30
    host=''
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
    P.canvasToData = P.canvasToRawData
    class ColorManagerConfig:
        ####
        #Sets gamma to BaseGamma + brightness * factor
        #This happens to improve the image quality, but it is not supported
        #by theory.
        redBaseGamma = 1.65
        greenBaseGamma = 1.55
        blueBaseGamma = 1.65
        redBrightnessFactor = 1.1
        greenBrightnessFactor = 1.2
        blueBrightnessFactor = 1.1
    import ColorManager as C
    convertColor = C.convertColorToLin


class LocalDisplayConfig:
    width = 60
    height = 30
    port = 5000
    normalize = True
    linearColorProfileCorretion = True
    class ColorManagerConfig:
        ####
        #Sets gamma to BaseGamma + brightness * factor
        #This happens to improve the image quality, but it is not supported
        #by theory.
        redBaseGamma = 2.4
        greenBaseGamma = 2.4
        blueBaseGamma = 2.4
        redBrightnessFactor = 0
        greenBrightnessFactor = 0
        blueBrightnessFactor = 0


class AudioServerConfig:
    port = 5001
    host = 'localhost'
    delay = -0.13
    alpha = 0.95
    maxBPS = 6

class InputServerConfig:
    port = 5002
    host = 'localhost'
    server = ''
    playerNumber = '1'

class PiDisplayConfig:
    width = 60
    height = 30
    port = 5000
    host = ''


