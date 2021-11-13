import pygame
from pygame.locals import *

from Transform import Transform
from Drawable import Drawable
from Manager import textureManager
from InputHandle import InputHandle

class Widget(Drawable, InputHandle):
    def __init__(self):
        self.transform = Transform()
        
class Bouton(Widget):
    def __init__(self, normal, hover, deasable, pressed):
        super(Bouton, self).__init__()

        self.normal = normal
        self.hover = hover
        self.deasable = deasable
        self.pressed = pressed

        self.transform.SetSize(100, 25)

        self.__Actual(self.normal)

    def __Actual(self, action):
        self.actuel = [action, textureManager.GetTexture(action[0])]
        if self.actuel[1] != None:
            self.actuel[1] = pygame.transform.smoothscale(self.actuel[1], (int(self.transform.size[0]), int(self.transform.size[1])))

    def SetPosition(self, x, y):
        self.transform.position = [x, y]

    def SetSize(self, w, h):
        self.transform.SetSize(w, h)
        self.__Actual(self.actuel[0])

    def GetSize(self):
        return self.transform.GetSize()

    def Scale(self, sx, sy, ox, oy):
        self.transform.Scale(sx, sy, ox, oy)
        self.__Actual(self.actuel[0])

    def SetScale(self, sx, sy):
        #self.transform.size[0] *= sx
        #self.transform.size[1] *= sy
        self.transform.SetScale(sx, sy)
        self.__Actual(self.actuel[0])

    def SetDeasable(self, deasable=True):
        if deasable:
            self.__Actual(self.deasable)
        else:
            self.__Actual(self.normal)

    def Render(self, game):
        if self.actuel[1] != None:
            x, y = self.transform.GetPosition()[0], self.transform.GetPosition()[1]
            w, h = self.transform.GetSize()[0], self.transform.GetSize()[1]

            game.screen.blit(self.actuel[1], (x, y, w, h))

    def EventInput(self, event):
        if self.actuel[0] != self.deasable:
            if event.type == MOUSEBUTTONDOWN:
                xs, ys = event.pos[0], event.pos[1]
                if self.transform.position[0] <= xs <= self.transform.position[0] + self.transform.size[0] and\
                    self.transform.position[1] <= ys <= self.transform.position[1] + self.transform.size[1]:
                    if self.actuel[0] != self.pressed:
                        self.__Actual(self.pressed)

                    action = self.actuel[0][1]
                    if action != None:
                        action()
            if event.type == MOUSEBUTTONUP and self.actuel[0] != self.hover:
                xs, ys = event.pos[0], event.pos[1]
                if self.transform.position[0] <= xs <= self.transform.position[0] + self.transform.size[0] and\
                    self.transform.position[1] <= ys <= self.transform.position[1] + self.transform.size[1]:
                    if self.actuel[0] != self.hover:
                        self.__Actual(self.hover)
                elif self.actuel[0] != self.normal:
                    self.__Actual(self.normal)
            if event.type == MOUSEMOTION:
                xs, ys = event.pos[0], event.pos[1]
                if self.transform.position[0] <= xs <= self.transform.position[0] + self.transform.size[0] and\
                    self.transform.position[1] <= ys <= self.transform.position[1] + self.transform.size[1]:
                    if self.actuel[0] != self.hover:
                        self.__Actual(self.hover)
                elif self.actuel[0] != self.normal:
                    self.__Actual(self.normal)

class Text(Widget):
    def __init__(self, text = "Default", size = 24, color = (0, 0, 0)):
        super(Text, self).__init__()
        self.police_name = None
        self.police_size = size
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(self.police_name, self.police_size)
        self.textImg = self.font.render(self.text, True, color)
        self.scale = [1, 1]
        self.transform.size = [self.textImg.get_size()[0] * self.scale[0], self.textImg.get_size()[1] * self.scale[0]]
        self.textDraw = pygame.transform.smoothscale(self.textImg,
                                                     (int(self.transform.size[0]), int(self.transform.size[1])))

    def SetText(self, text):
        self.text = text
        self.textImg = self.font.render(self.text, True, self.color)
        self.transform.size = [self.textImg.get_size()[0] * self.scale[0], self.textImg.get_size()[1] * self.scale[0]]
        self.textDraw = pygame.transform.smoothscale(self.textImg,
                                                     (int(self.transform.size[0]), int(self.transform.size[1])))

    def SetFont(self, name=None, size=None):
        if size != None:
            self.police_size = size
        if name != None:
            self.police_name = name
        self.font = pygame.font.SysFont(self.police_name, self.police_size)
        self.textImg = self.font.render(self.text, True, self.color)
        self.transform.size = [self.textImg.get_size()[0] * self.scale[0], self.textImg.get_size()[1] * self.scale[0]]
        self.textDraw = pygame.transform.smoothscale(self.textImg,
                                                     (int(self.transform.size[0]), int(self.transform.size[1])))

    def SetColor(self, color):
        self.color = color
        self.textImg = self.font.render(self.text, True, self.color)
        self.transform.size = [self.textImg.get_size()[0] * self.scale[0], self.textImg.get_size()[1] * self.scale[0]]
        self.textDraw = pygame.transform.smoothscale(self.textImg,
                                                     (int(self.transform.size[0]), int(self.transform.size[1])))

    def Render(self, game):
        x, y = self.transform.position[0], self.transform.position[1]
        w, h = self.transform.size[0], self.transform.size[1]
        game.screen.blit(self.textDraw, (x, y, w, h))

    def SetScale2(self, sx, sy):
        self.scale[0] *= sx
        self.scale[1] *= sy
        self.transform.size[0] *= sx
        self.transform.size[1] *= sy

        self.textDraw = pygame.transform.smoothscale(self.textImg, (int(self.transform.size[0]), int(self.transform.size[1])))

    def Reset(self):
        self.textDraw = pygame.transform.smoothscale(self.textImg,
                                                     (int(self.transform.size[0]), int(self.transform.size[1])))