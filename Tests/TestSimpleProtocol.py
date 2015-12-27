import Transportation.Protocol.SimpleProtocol as P
import random


def main():
    height =10
    width =5
    rgb= [tuple([getRandom(),getRandom(),getRandom()]) for i in range(0, 3*height*width, 3)]
    colorArray=[rgb[i:i+width] for i in range(0, height*width, width)]
    
    print colorArray
    data= P.colorArrayToData(colorArray)
    assert(P.dataToColorArray(data)==colorArray)
def getRandom():
    return random.randint(0, 255)

