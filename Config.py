curtain = ""
useImages = False
useAudio = True
import ScreenCanvasArray 
Canvas = ScreenCanvasArray.Canvas

if curtain=="old":
    width = 15
    height = 5
    host='10.0.63.101'
    port=6038
    import Transportation.Protocol.OldProtocol as P
    Protocol = P
    import ColorManager as C
    convertColor = C.convertColorToLin #Converts the color profile to linear

elif curtain=='local': #Assume local
    width = 60
    height = 30
    host='localhost'
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
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
    import ColorManager as C
    convertColor = C.convertColorToLin

elif curtain=='other': #???
    width = 60
    height = 30
    host=''#write host here
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
    import ColorManager as C
    convertColor = C.convertColorToLin

elif curtain=='otherPi': #???
    width = 60
    height = 30
    host=''#write host here
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
    P.canvasToData = P.canvasToRawData
    import ColorManager as C
    convertColor = C.convertColorToLin

class LocalDisplayConfig:
    width = 60
    height = 30
    port = 5000
    normalize = True
    linearColorProfileCorretion = True


class AudioServerConfig:
    port = 5001
    host = 'localhost'
    delay = -0.03
    alpha = 0.95
    maxBPS = 6

class PiDisplayConfig:
    width = 60
    height = 30
    port = 5000
    host = ''

