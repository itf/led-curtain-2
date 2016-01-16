curtain = "local"

if curtain=="old":
    width = 15
    height = 5
    host='10.0.63.101'
    port=6038
    import Transportation.Protocol.OldProtocol as P
    Protocol = P
    import ColorManager as C
    convertColor = C.convertColorToLin #Converts the color profile to linear
else: #Assume local
    width = 60
    height = 30
    host='localhost'
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
    import ColorManager as C
    convertColor = C.convertColorToLin  #Converts the color profile to linear

class LocalDisplayConfig:
    width = 60
    height = 30
    port = 5000
    normalize = True
    linearColorProfileCorretion = True
