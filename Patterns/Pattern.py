'''Based on https://github.com/FirstEast/1e-Disco/blob/master/server/pattern/pattern.py'''

import time
import random

class PatternInfo():
    def __init__(self,displayWidth, displayHeight, frameNumber = 0, audioInfo =None, params={})
        self

class Pattern():
  '''
  Top level pattern class. Defines basic parameter setting and render function.
  '''

  DEFAULT_PARAMS = {
    # Your default parameters, such as:
    # 'Main Color': Color([255,0,0])
    #
    # If this dict is empty, your Pattern will not appear in the web UI.
    #
    # If a param is a list of some sort, then don't mutate the list in your
    # own params dict. Assign a new one. Copying objects is not easy children.
    #
    # Note: do not set default parameters to None
  }
  
  INTERACTIVE_PARAM_TYPES={
    #String, INT, Function, etc.
    #It will be used by the UI to decide what parameters to show
    #An int parameter will be a scrollbar
    #A string parameter a textbox
    #Example: Render text receives a string
    #Visualize audio bars receive the int that represents the height of the bars
    #Single color receives 3 ints representing colors RGB
  }
  def __init__(self, params=DEFAULT_PARAMS):
    self.params = params
    
    self.initialize()

  def initialize(self):
    pass
    
  def render(self, displayWidth, displayHeight, frameNumber = 0, audioInfo =None, params={}):
    '''
    Returns the specified pattern at frame frameNumber. When frame numbers are not well
    defined, returns the next step on the pattern based on the other values.
    
    '''
    pass



class StaticPattern(Pattern):
  '''
  Static Pattern class. Handles caching of frames for static patterns.
  Children must implement renderNew.
  '''

  def __init__(self, params={}):
    Pattern.__init__(self, params)
    self.newParams = True
    self.frame = None

  def paramUpdate(self, paramName):
    self.newParams = True

  def render(self, device):
    if self.newParams:
      self.frame = self.renderFrame(device)
      self.newParams = False
    return self.frame.copy()

  def renderFrame(self, device):
    '''
    Returns frame based on the set parameters. Only called when params change.
    '''
    pass  

class TimedPattern(Pattern):
  '''
  Timed Pattern class. Handles frame counting based on real world time.
  Used for time variant looping patterns.
  Children of this class must implement the renderFrame function, which will
  be called with a frame number argument and the device.
  '''
  START_TIME = time.time() * 1000
  DEFAULT_RATE = 30 #FPS
  DEFAULT_PATTERN=Pattern #OVERRIDE and put a class
  DEFAULT_PARAMS = {
    'Rate': DEFAULT_RATE,
    'UpdateFrame': lambda time, lastTime: (time-lasTime)>float(1000.0 / self.params['Rate'])
  }

  def __init__(self, params=DEFAULT_PARAMS):
    self.params=params
    self.pattern=self.DEFAULT_PATTERN(params)
    self.lastTime = self.START_TIME
    self.frame = 0
    self.previousFrame=1
    self.alreadyRendered=False
    
  def render(self, displayWidth, displayHeight, frameNumber = 0, audioInfo =None, params=DEFAULT_PARAMS):
        if (self.alreadyRendered):
            thisTime = time.time() * 1000
            inc = int((thisTime - self.lastTime) / float(1000.0 / int(self.params['Rate'])))
            if inc > 0:
                self.frame += inc
                self.lastTime = thisTime
            else:
                return self.previousFrame
        self.previousFrame= self.pattern.render((displayWidth, displayHeight), self.getFrameCount(), audioInfo, params)
        self.alreadyRendered=True
        return self.previousFrame
    

