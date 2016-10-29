import copy
from array import array as array
class Canvas:
    '''
    Array Implementation of canvas
    All the mod operations that look convoluted are here because
    they were considerably faster than loops
    '''
    def __init__(self,height, width, previousArray=None):
        if (previousArray is None):
            self._array = [0. for x in xrange(3*width * height)]
        else:
            self._array = previousArray
        self.height=height
        self.width=width
        self.pendingMappingFunctions=[]

        self.startX=[0]
        self.startY=[0]
        self._heightArr=[height]
        self._widthArr=[width]
        self._setArray = self._array
        self._standardSet = self.__setitem__
        self._standardApply = self.mapFunctionApply
        self._convertYX = self._getConvertYXPosFunction()

    def __getitem__(self, arg):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        y,x = arg
        pos=self._convertYX(y,x)
        return self._array[pos:pos+3]

    def getArray(self):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        return self._array

    def __setitem__(self,arg,value):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        y,x = arg
        pos=self._convertYX(y,x)
        self._setArray[pos],self._setArray[pos+1],self._setArray[pos+2] = value[0],value[1],value[2]

    def mapFunction(self,function):
        self.pendingMappingFunctions.append(function)
    
    def mapFunctionApply(self):
        '''
        Optimized for performance
        '''
        height=self._heightArr[-1]
        width=self._widthArr[-1]
        getArray=self._array
        setArray = self._setArray
        
        convertYX=self._convertYX
        for y in xrange(height):
            for x in xrange(width):
                pos = convertYX(y,x)
                r,g,b = getArray[pos:pos+3]
                for function in self.pendingMappingFunctions:
                    r,g,b= function((r,g,b), y, x)
                setArray[pos], setArray[pos+1], setArray[pos+2] = r,g,b
        self.pendingMappingFunctions=[]

    def translateAndScale(self,x=None,y=None,height=None,width=None):
        if (x==None):
            x=0
        self.startX.append(x)
        if (y==None):
            y=0
        self.startY.append(y)
        if (height==None):
            height=self._heightArr[-1]
        self._heightArr.append(max(1,min(height,self._heightArr[-1])))
        if (width==None):
            width=self._widthArr[-1]
        self._widthArr.append(max(1,min(width,self._widthArr[-1])))
        self._convertYX = self._getConvertYXPosFunction()


    def restoreTranslateAndScale(self, clear=True):
        if clear:
            self.eraseNonDisplayable()
        self.mapFunctionApply()
        self.startX.pop()
        self.startY.pop()
        self._heightArr.pop()
        self._widthArr.pop()
        self._convertYX = self._getConvertYXPosFunction()

        
    def getByte(self, y,x):
        return _floatToByte(self[y,x])


    def _getConvertYXPosFunction(self):
        x0s=self.startX
        y0s=self.startY
        heights=self._heightArr
        widths=self._widthArr
        length = len(heights)-1
        realHeight = self.height
        realWidth = self.width
        def convertYX(y,x):
            for n in xrange(length,-1,-1):
                y%=heights[n]
                x%=widths[n]
                x=(x+x0s[n])
                y=(y+y0s[n])
            pos = (y*realWidth+x)*3
            return pos
        def convertYXSimple(y,x):
            y%=realHeight
            x%=realWidth
            pos = (y*realWidth+x)*3
            return pos

        if len(x0s)>1:
            return convertYX
        else:
            return convertYXSimple


    def eraseNonDisplayable(self):
        posSet=set()
        height=self._heightArr[-1]
        width=self._widthArr[-1]
        convertYX=self._getConvertYXPosFunction()
        x=0
        y=0
        for i in xrange(height*width):
            y%=height
            x%=width
            pos = convertYX(y,x)
            posSet.add(pos)
            x+=1
            y+=int(x)/width
        realHeight = self.height
        realWidth = self.width
        myArray=self._array
        for i in xrange(realHeight*realWidth):
            pos = i*3
            if pos not in posSet:  
                myArray[pos], myArray[pos+1], myArray[pos+2] = 0,0,0
        
    def updateArgs(self, otherCanvas):
        self._widthArr = copy.deepcopy(otherCanvas._widthArr)
        self._heightArr = copy.deepcopy(otherCanvas._heightArr)
        self.startX = copy.deepcopy(otherCanvas.startX)
        self.startY = copy.deepcopy(otherCanvas.startY)
        convertYX=self._convertYX


    def _floatToByte(self, f):
        return max(min(255,int(f*255+0.5)),0)


    #############3
    def copyArray(self, otherCanvas):
        otherArray = otherCanvas._array
        for i in xrange(len(otherArray)):
            self._array[i] = otherArray[i]


    def __deepcopy__(self,memo):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        newColorarray = self._array*1
        newone=Canvas(self.height,self.width,newColorarray)
        newone.pendingMappingFunctions=[]
        newone._convertYX = self._convertYX
        newone._widthArr = copy.deepcopy(self._widthArr)
        newone._heightArr = copy.deepcopy(self._heightArr)
        newone.startX = copy.deepcopy(self.startX)
        newone.startY = copy.deepcopy(self.startY)
        return newone
