from Display.Pygame.pgCurtain import PygameCurtain
import time
import random
height =10;
width = 5;
def main():
    curtain = PygameCurtain(width,height)
    color={}
    for i in xrange(25):
        color[(random.randint(0, width-1),random.randint(0, height-1))]=(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        curtain.sendColorDict(color)
        time.sleep(0.1)
    for i in xrange(25):
        rgb= [tuple([getRandom(),getRandom(),getRandom()]) for i in range(0, 3*height*width, 3)]
        colorArray=[rgb[i:i+width] for i in range(0, height*width, width)]
        curtain.sendColorArray(colorArray)
        time.sleep(0.1)

def getRandom():
    return random.randint(0, 255)
