import ScreenCanvasArray as Canvas

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
    convert = lambda x: chr(max(min(255,x),0))
    return[convert(x) for colorRow in colorArray for _tuple in colorRow for x in _tuple]


def canvasToData(canvas):
    height = canvas.height
    width = canvas.width
    data = str(width)+'#'+str(height)+'#'+(''.join(canvasToString(canvas)))
    return data

def canvasToString(canvas):
    convert = lambda x: chr(max(min(255,int(round(255*x))),0))
    height = canvas.height
    width = canvas.width
    return[convert(color) for y in xrange(height) for x in xrange(width)  for color in canvas[y,x]]


def dataToCanvas(data):
    width, height, colors = data.split('#',2)
    width, height = int(width), int(height)
    rgb= [tuple(map(ord,colors[i:i+3])) for i in range(0, 3*height*width, 3)]
    canvas = Canvas.Canvas(width = width, height = height)
    index=0
    for i in xrange(height):
        for j in xrange(width):
            canvas[i,j]=rgb[index]
            index+=1
    return canvas
            
