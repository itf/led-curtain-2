'''
Based on jrafidi code. Can be found on
https://github.com/FirstEast/1e-Disco/blob/master/server/pattern/static/image.py

And using part of BiggleZX code, found on
https://gist.github.com/BigglesZX/4016539
'''
import Patterns.Pattern as P
import Patterns.Function as F
import Config

if Config.useImages:
    from PIL import Image
    from os import listdir
    imagePath = "Patterns/ExtraPatterns/images/"
    import glob

def simpleCached(cacheSize):
    cache={}
    def cacheFunction(function):
        def cachedFunction(*args):
            tArgs=tuple(args)
            if tArgs in cache:
                return cache[tArgs]
            else:
                answer=function(*args)
                if len(cache)>cacheSize:
                    cache.popitem()
                    cache.popitem()
                cache[tArgs]=answer
                return answer
        return cachedFunction
    return cacheFunction



@P.pattern("image")
@F.defaultArgsP(imageName = "pacman.gif",
                imageHeight = 1,
                imageWidth = 1)
def imagePattern(PatternInput):
    if Config.useImages:
        imageName = PatternInput['imageName']
        imageHeight = PatternInput['imageHeight']
        imageWidth = PatternInput['imageWidth']
        height = PatternInput['height']
        width = PatternInput['width']
        frame = PatternInput['frame']

        fullPath=imagePath+imageName
        imageYpixels = int(height*imageHeight)
        imageXpixels = int(width*imageWidth)
        
        imageFrames=getGifFrames(fullPath, imageYpixels, imageXpixels)
        nFrames= len(imageFrames)
        imageFrameNumber = frame%nFrames
        imageFrame = imageFrames[imageFrameNumber]

        maxX=imageXpixels
        maxY= imageYpixels
        def imager(rgb,y,x):
            if y<maxY and x<maxX:
                r,g,b=imageFrame.getpixel((x,y))[0:3]
                return (r/255.,g/255.,b/255.)
            else:
                return (0,0,0)
        canvas=PatternInput["canvas"]
        canvas.mapFunction(imager)
    
    return PatternInput

###################################
#Slightly modified BiggleZX code, found on
#https://gist.github.com/BigglesZX/4016539
@simpleCached(5)
def getGifFrames(imagePath, height, width):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(imagePath)['mode']
    
    im = openImage(imagePath)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    frames=[]
    try:
        while True:

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('RGBA', im.size)
            
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            frames.append(new_frame.resize((width, height), Image.NEAREST))

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        return frames
        pass

@simpleCached(5)
def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    im = openImage(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

####################
#End of BiggleZX code

def openImage(imagePath):
    try:
        im = Image.open(imagePath)
    except:
        try:
            filename = glob.glob(imagePath + '.*')[0]
            im = Image.open(filename)
        except:
            filename = glob.glob(imagePath + '*')[0]
            im = Image.open(filename)
    return im
   
