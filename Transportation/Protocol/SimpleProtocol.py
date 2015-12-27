def commandToString(command, data):
    return command + '#' + data

def colorArrayToData(colorArray):
    height = len(colorArray)
    if (height>0):
        width= len(colorArray[0])
    else:
        width = 0
    data = str(width)+'#'+str(height)+'#'+(''.join(colorArrayToString(colorArray)))
    return data

#Assumes the array to be an array of tuples.
def dataToColorArray(data):
    width, height, colors = data.split('#',2)
    width, height = int(width), int(height)
    rgb= [tuple(map(ord,colors[i:i+3])) for i in range(0, 3*height*width, 3)]
    colorArray=[rgb[i:i+width] for i in range(0, height*width, width)]
    return colorArray

def colorDictToString(colorDict):
    raise Exception("Not Implemented")

def colorArrayToString(colorArray):
    return[chr(x) for colorRow in colorArray for _tuple in colorRow for x in _tuple]
