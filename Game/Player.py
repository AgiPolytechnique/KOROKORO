import random
import time

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

    def GetItem(self, index):
        if 0 <= index < len(self.textureName):
            return self.textureName[index]
        return None

class Grid(Entity):
    def __init__(self):
        super(Grid, self).__init__()
            
class Player(Entity):
    def __init__(self, adversaire = None):
        super(Player, self).__init__()
        self.adversaire = adversaire

        self.quantiter = 0
        self.nom_coup = 0
        self.possibiliter = []

    def AddPossibility(self, possibility):
        if possibility in self.possibiliter:
            return
        self.possibiliter.append(possibility)

    def RemovePossibility(self, possibility):
        if possibility in self.possibiliter:
            self.possibiliter.remove(possibility)

    def RemovePossibilityArray(self, possibility):
        for p in possibility:
            self.RemovePossibility(p)

    def AddPossibilityArray(self, array):
        for p in array:
            self.AddPossibility(p)

    def GetPossibilityCopy(self):
        return self.possibiliter.copy()

    def Reset(self):
        self.quantiter = 0
        self.nom_coup = 0

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

    def SetProfondeur(self, profondeur):
        self.profondeur = profondeur

    def FonctionEvaluation(self, map, profondeur, maximise, i, j, grid):
        gain = gameLogics.Logics(i, j, map, self, grid)
        return len(gain[0]) if gain != [] else 0

    def PlusInfini(self):
        return 1000

    def MoinInfini(self):
        return -1000

    def Play(self, map, grid):
        self.playPosition = self.glouton(map, grid)
        self.flex_state = "finish"

    def glouton(self, map, grid):
        max_ = self.MoinInfini()

        ligne, colone = -1, -1
        for i in range(len(map)):
            for j in range(len(map[0])):
                m = map.copy()
                evaluation = self.FonctionEvaluation(map, 0, True, i, j, grid)
                map = m
                if max_ < evaluation or (max_ == evaluation and random.randint(1, 100) < 50):
                    max_ = evaluation
                    ligne = i
                    colone = j
        return [ligne, colone]

    def minimax(self, node, depth, maximizingPlayer):
        if depth == 0 or len(node) <= 0:
            return