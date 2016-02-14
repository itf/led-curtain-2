import copy
from array import array as array
class Canvas:
    '''
    Array Implementation of canvas
    '''
    def __init__(self,height, width, previousArray=None):
        if (previousArray==None):
            self._array = array('f',[0. for x in xrange(3*width) for y in xrange(height)])
        else:
            self._array=array('f',previousArray)
        self.height=height
        self.width=width
        self.pendingMappingFunctions=[]

        self.startX=[0]
        self.startY=[0]
        self._heightArr=[height]
        self._widthArr=[width]
        
    def __getitem__(self, arg):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        convertYX=self._getConvertYXPosFunction()
        y,x = arg
        pos=convertYX(y,x)
        return self._array[pos:pos+3]

    def __setitem__(self,arg,value):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        y,x = arg
        convertYX=self._getConvertYXPosFunction()
        pos=convertYX(y,x)
        self._array[pos],self._array[pos+1],self._array[pos+2] = value[0],value[1],value[2]

    def mapFunction(self,function):
        self.pendingMappingFunctions.append(function)
    
    def mapFunctionApply(self):
        '''
        Optimized for performance
        '''
        height=self._heightArr[-1]
        width=self._widthArr[-1]
        y=0
        x=0
        myArray=self._array
        
        convertYX=self._getConvertYXPosFunction()
        for i in xrange(height*width):
            y%=height
            x%=width
            pos = convertYX(y,x)
            r,g,b = myArray[pos:pos+3]
            for function in self.pendingMappingFunctions:
                r,g,b= function((r,g,b), y, x)
            myArray[pos], myArray[pos+1], myArray[pos+2] = r,g,b
            x+=1
            y+=int(x)/width
        self.pendingMappingFunctions=[]

    def translateAndScale(self,x=None,y=None,height=None,width=None):
        previousHeight = self._heightArr[-1]
        previousWidth =self._widthArr[-1]
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
    def restoreTranslateAndScale(self):
        self.eraseNonDisplayable()
        self.mapFunctionApply()
        self.startX.pop()
        self.startY.pop()
        self._heightArr.pop()
        self._widthArr.pop()
        
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
            xi=(x)%realWidth
            yi=(y)%realHeight
            pos = (y*realWidth+x)*3
            return pos
        return convertYX

    

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
            
        

    def _floatToByte(self, f):
        return max(min(255,round(f*255)),0)
    def __deepcopy__(self,memo):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        height=self.height
        width=self.width
        newColorarray=copy.deepcopy(self._array)
        newone=Canvas(self.height,self.width,newColorarray)
        newone.pendingMappingFunctions=[]
        newone._widthArr = copy.deepcopy(self._widthArr)
        newone._heightArr = copy.deepcopy(self._heightArr)
        newone.startX = copy.deepcopy(self.startX)
        newone.startY = copy.deepcopy(self.startY)
        return newone
