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
        
    def __getitem__(self, arg):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        width=self.width
        y,x = arg
        pos=(y*width+x)*3
        return self._array[pos],self._array[pos+1],self._array[pos+2]

    def __setitem__(self,arg,value):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        width=self.width
        y,x = arg
        pos=(y*width+x)*3
        self._array[pos],self._array[pos+1],self._array[pos+2] = value[0],value[1],value[2]

    def mapFunction(self,function):
        self.pendingMappingFunctions.append(function)
    
    def mapFunctionApply(self):
        '''
        Optimized for performance
        '''
        height=self.height
        width=self.width
        myArray=self._array
        y=0
        x=-1
        for i in xrange(height*width):
            x+=1
            y+=int(x)/width
            x%=width
            pos =3*i
            r,g,b = myArray[pos], myArray[pos+1], myArray[pos+2]
            for function in self.pendingMappingFunctions:
                r,g,b= function((r,g,b), y, x)
            myArray[pos], myArray[pos+1], myArray[pos+2] = r,g,b
        self.pendingMappingFunctions=[]
        
    def getByte(self, y,x):
        return _floatToByte(self[y,x])

    def _floatToByte(self, f):
        return max(min(255,round(f*255)),0)
    def __deepcopy__(self,memo):
        if self.pendingMappingFunctions:
            self.mapFunctionApply()
        height=self.height
        width=self.width
        newColorarray=copy.deepcopy(self._array)
        newone=Canvas(self.height,self.width,newColorarray)
        return newone
