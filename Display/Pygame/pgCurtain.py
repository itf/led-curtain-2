import pygame
import sys
import math
from Display.DisplayInterface import DisplayInterface as DisplayInterface

# Coordinates of broken pixels on the curtain.
BROKEN_PIXELS_ALL = []
BROKEN_PIXELS_RED = []
BROKEN_PIXELS_GREEN = []
BROKEN_PIXELS_BLUE = []

DEFAULT_WINDOWS_SIZE=300,300
CELL_PADDING_RATIO = 6 
class Cell(object):
    def __init__(self, position, size, padding):
        self.position = position
        self.size = size
        self.padding = padding
        self.rect = pygame.Rect((
            self.position[0] * self.size,
            self.position[1] * self.size,
            ),(
            self.size - self.padding,
            self.size - self.padding,
        ))
        self.color = 150, 0, 0

    def setColor(self, r, g, b):
        if self.position in BROKEN_PIXELS_ALL:
            r, g, b = 0, 0, 0
        if self.position in BROKEN_PIXELS_RED:
            r = 0
        if self.position in BROKEN_PIXELS_GREEN:
            g = 0
        if self.position in BROKEN_PIXELS_BLUE:
            b = 0
        self.color = r, g, b


class PygameCurtain(object,DisplayInterface):
    def __init__(self, width, height):
        # measurements in cells
        self.size_cells = width, height
        self.width = width
        self.height = height

        # measurements in pixels
        self._resizeScreen(DEFAULT_WINDOWS_SIZE)

        # initialize grid of cells
        self.cells = [[
            Cell((x,y), size=self.cell_scale, padding=self.cell_padding)
            for y in xrange(self.size_cells[1])]
            for x in xrange(self.size_cells[0])
        ]

        self._renderCells()
    def _resizeScreen(self,size_px):
        self.size_px = size_px
        self.screen = pygame.display.set_mode(self.size_px, pygame.RESIZABLE)
        self.cell_scale = min(self.size_px[0]/self.width,self.size_px[1]/self.height)
        self.cell_padding = self.cell_scale/CELL_PADDING_RATIO
        
    def _renderCells(self):
        for x in xrange(self.width):
            for y in xrange(self.height):
                cell = self.cells[x][y]
                pygame.draw.rect(self.screen, cell.color, cell.rect)

    def sendColorDict(self, color_dict):
        self._processEvents()
        """
        Render the `color_dict`.

        `color_dict` is a dict where the keys are tuples
        in the bounds of `width` and `height` and the values
        are tuples of r, g, b.
        """
        # for (x, y), (r, g, b) in color_dict:
        #     print x, y, r, g, b
        # for foo in color_dict.items():
        #     print foo
        #     print type(foo)
        for (x, y), (r, g, b) in color_dict.items():
            self.cells[x][y].setColor(r, g, b)

        self._renderCells()
        pygame.display.flip()
        
    def sendColorArray(self, colorArray):
        #colorArray is an array of (r,g,b)
        self._processEvents()
        lenHeight = min(len(colorArray), self.height)
        for i in xrange(lenHeight):
            row = colorArray[i] 
            lenWidth = min(len(row),self.width)
            for j in xrange(lenWidth):
                (r,g,b) = colorArray[i][j]
                self.cells[j][i].setColor(r, g, b)

        self._renderCells()
        pygame.display.flip()
    def _processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self._resizeScreen(event.size)
                for cellrow in self.cells:
                    for cell in cellrow:
                        cell.size = self.cell_scale
                        cell.padding = self.cell_padding
                        cell.rect.x = cell.position[0] * cell.size
                        cell.rect.y = cell.position[1] * cell.size
                        cell.rect.width = cell.size - cell.padding
                        cell.rect.height = cell.size - cell.padding
