import math

class Transform:
    def __init__(self):
        self.position = [0, 0]
        self.size = [0, 0]
        self.origine = [0, 0]

        self.rotation = 0
        self.scale = [1, 1]

    def GetPosition(self):
        return self.position

    def SetPosition(self, x, y):
        x1 = -self.position[0] + self.origine[0]
        y1 = -self.position[1] + self.origine[1]
        self.origine = [x + x1, y + y1]
        self.position = [x, y]

    def GetSize(self):
        return self.size

    def SetSize(self, w, h):
        self.size = [w, h]

    def GetOrigine(self):
        return self.origine

    def SetOrigine(self, x=0, y=0, type=None):
        if type == None:
            self.origine = [x, y]
        else:
            if type == "center":
                self.origine = [self.position[0] + self.size[0]/2, self.position[1] + self.size[1]/2]

    def Move(self, x, y):
        self.position[0] += x
        self.position[1] += y
        self.origine[0] += x
        self.origine[1] += y

    def Scale(self, sx, sy, ox = None, oy = None):
        o = [self.origine[0] if ox == None else ox, self.origine[1] if oy == None else oy]
        self.scale = [self.scale[0]*sx, self.scale[1]*sy]
        self.__Scale(o)

    def SetScale(self, sx, sy, ox = None, oy = None):
        o = [self.origine[0] if ox == None else ox, self.origine[1] if oy == None else oy]
        self.scale = [sx, sy]
        self.__Scale(o)

    def __Scale(self, origine):
        self.size = [self.size[0]*self.scale[0], self.size[1]*self.scale[1]]

        self.position[0] = self.position[0] * self.scale[0] + (1 - self.scale[0])*origine[0]
        self.position[1] = self.position[1] * self.scale[1] + (1 - self.scale[1])*origine[1]
        
        self.origine[0] = self.origine[0] * self.scale[0] + (1 - self.scale[0]) * origine[0]
        self.origine[1] = self.origine[1] * self.scale[1] + (1 - self.scale[1]) * origine[1]

    def Rotation(self, a, ox = None, oy = None):
        self.rotation += a
        o = [self.origine[0] if ox == None else ox, self.origine[1] if oy == None else oy]
        self.__Rotation(o)

    def SetRotation(self, a, ox = None, oy = None):
        self.rotation += a
        o = [self.origine[0] if ox == None else ox, self.origine[1] if oy == None else oy]
        self.__Rotation(o)

    def __Rotation(self, origine):
        self.position[0] = self.position[0] * math.cos(self.rotation) - self.position[1] * \
                           math.sin(self.rotation) + (1 - origine[0]) * math.cos(self.rotation) + \
                           origine[1] * math.sin(self.rotation)
        self.position[1] = self.position[0] * math.sin(self.rotation) - self.position[1] * \
                           math.cos(self.rotation) + (1 - origine[1]) * math.cos(self.rotation) - \
                           origine[0] * math.sin(self.rotation)

        self.origine[0] = self.origine[0] * math.cos(self.rotation) - self.origine[1] * \
                           math.sin(self.rotation) + (1 - origine[0]) * math.cos(self.rotation) + \
                           origine[1] * math.sin(self.rotation)
        self.origine[1] = self.origine[0] * math.sin(self.rotation) - self.origine[1] * \
                           math.cos(self.rotation) + (1 - origine[1]) * math.cos(self.rotation) - \
                           origine[0] * math.sin(self.rotation)

    def Apply(self):
        self.__Scale(self.origine)
        self.__Rotation(self.origine)