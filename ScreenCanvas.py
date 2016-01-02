class Canvas:
    '''
    Nice abstraction to work on a Canvas.
    Used by Display, Transportation and Patterns

    It is the output of a pattern

    At the moment it uses a list of lists, but the implementation
    may change to use a numpy matrix, or an Array for performance reasons

    The values of the color channels on the canvas should be floats from 0 to 1.
    '''
    def __init__(self,height, width):
        self._colorArray = [[(0,0,0) for x in xrange(width)] for y in xrange(height)]
        self.height=height
        self.width=width
    def __getitem__(self, arg):
        if isinstance(arg,tuple):
            y,x = arg
            return self.getRow(y)[x]
        else:
            y=arg
            return self.getRow(y)

    def __setitem__(self,arg,value):
        if isinstance(arg,tuple):
            y,x = arg
            rowY= self.getRow(y)
            rowY[x]= value
        else:
            y=arg
            rowY= self.getRow(y)
            rowY=value
    def getRow(self, y):
        return self._colorArray[y]

    def mapFunction(self,function):
        for y in xrange(self.height):
            for x in xrange(self.width):
                self[y,x]=function(self[y,x], y, x)

    def getByte(self, y,x):
        return _floatToByte(self[y,x])

    def _floatToByte(self, f):
        return max(min(255,round(f*255)),0)
