import random

from GameLogics import gameLogics


class Entity:
    id = 0
    def __init__(self):
        self.id = Entity.id
        Entity.id += 1

        self.textureName = []
        self.activeTexture = -1

    def GetId(self):
        return self.id

    def AddTexture(self, name):
        self.textureName.append(name)
        if len(self.textureName) == 1:
            self.activeTexture = 0

    def Next(self):
        self.activeTexture += 1
        if self.activeTexture >= len(self.textureName):
            self.activeTexture = 0 if len(self.textureName)>0 else -1

    def Previous(self):
        self.activeTexture -= 1
        if self.activeTexture < 0:
            self.activeTexture = len(self.textureName) - 1 if len(self.textureName) > 0 else -1

    def SetActiveTexture(self, index):
        if 0 <= index < len(self.textureName):
            self.activeTexture = index

    def GetActive(self):
        return self.textureName[self.activeTexture]

class Grid(Entity):
    def __init__(self):
        super(Grid, self).__init__()
            
class Player(Entity):
    def __init__(self, adversaire = None):
        super(Player, self).__init__()
        self.adversaire = adversaire

        self.quantiter = 0

    def SetAdversair(self, adversaire):
        self.adversaire = adversaire

    def GetAdversaire(self):
        return self.adversaire

    def AddQuantiter(self, q = 1):
        self.quantiter += q

    def RemoveQuantiter(self, q = 1):
        self.quantiter -= q

class Human(Player):
    def __init__(self, adversaire):
        super(Human, self).__init__(adversaire)
        
class IA(Player):
    def __init__(self, adversaire):
        super(IA, self).__init__(adversaire)
        self.profondeur = 0

        self.flex_state = "begin"

        self.playPosition = [None, None]

        self.possibiliter = []

    def AddPossibiliter(self, x, y):
        self.possibiliter.append([x, y])

    def AddPossibiliterArray(self, array):
        for p in array:
            self.AddPossibiliter(p[0], p[1])

    def RemovePossibiliter(self, x, y):
        if [x, y] in self.possibiliter:
            self.possibiliter.remove([x, y])

    def FonctionEvaluation(self, map, profondeur, maximise, i, j):
        return len(gameLogics.Logics(i, j, map, self))

    def PlusInfini(self):
        return 1000

    def MoinInfini(self):
        return -1000

    def Play(self, map):
        self.playPosition = self.glouton(map)
        self.flex_state = "finish"

    def glouton(self, map):
        max_ = self.MoinInfini()

        ligne, colone = -1, -1
        '''for pos in self.possibiliter:
            if 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0]):
                m = map.copy()
                evaluation = self.FonctionEvaluation(map, 0, True, pos[0], pos[1])
                map = m
                if max_ < evaluation or (max_ == evaluation and random.randint(1, 100) < 50):
                    max_ = evaluation
                    colone, ligne = pos[1], pos[0]'''
        for i in range(len(map)):
            for j in range(len(map[0])):
                m = map.copy()
                evaluation = self.FonctionEvaluation(map, 0, True, i, j)
                map = m
                if max_ < evaluation or (max_ == evaluation and random.randint(1, 100) < 50):
                    max_ = evaluation
                    colone, ligne = j, i
        return [ligne, colone]