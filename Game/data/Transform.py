

class Transform:
    def GetPosition(self):
        return self.position

    def SetPosition(self, x, y):
        self.position = [x, y]

    def GetSize(self):
        return self.size

    def SetSize(self, w, h):
        self.size = [w, h]

    def GetOrigine(self):
        return self.origine

    def SetOrigine(self, x, y):
        self.origine = [x, y]

    def Move(self, x, y):
        self.position = [self.position[0] + x, self.position[y] + y]

    def Scale(self, sx, sy, ox = None, oy = None):
        o = self.origine
        if ox != None:
            o[0] = ox
        if oy != None:
            o[1] = oy
        self.position[0] = sx*self.position[0] + (1-sx)*o[0]
        self.position[1] = sy*self.position[1] + (1-sy)*o[1]

        self.size[0] = sx * self.size[0] + (1 - sx) * o[0]
        self.size[1] = sy * self.size[1] + (1 - sy) * o[1]

        self.origine[0] = sx * self.origine[0] + (1 - sx) * o[0]
        self.origine[1] = sy * self.origine[1] + (1 - sy) * o[1]

    def rotation(self, r, ox = None, oy = None):
        o = self.origine
        if ox != None:
            o[0] = ox
        if oy != None:
            o[1] = oy