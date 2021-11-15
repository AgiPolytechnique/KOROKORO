

class GameLogis:
    def Logics(self, n, m, map, player, grid):
        #print([n, m])
        map_copy = map.copy()
        if 0 <= n < len(map_copy) and 0 <= m < len(map_copy[0]) and map_copy[n][m] == grid.GetId():
            heat = False
            gain = [[n, m]]
            map_copy[n, m] = player.GetId()
            for i in range(n-1, n+2):
                for j in range(m-1, m+2):
                    if 0 <= i < len(map_copy) and 0 <= j < len(map_copy[0]):
                        if (not heat) and map[i][j] == player.GetId():
                            heat = True
                        elif map[i][j] == player.GetAdversaire().GetId():
                            gain.append([i, j])
                            map_copy[i, j] = player.GetId()
            possibiliter = []
            for g in gain:
                for i in range(g[0] - 1, g[0] + 2):
                    for j in range(g[1] - 1, g[1] + 2):
                        if 0 <= i < len(map_copy) and 0 <= j < len(map_copy[0]) and map[i][j] == grid.GetId():
                            possibiliter.append([i, j])
            if heat:
                return [gain, possibiliter]
        return []

    def GameFinish(self, map, player, grid):
        for i in range(len(map)):
            for j in range(len(map[0])):
                gain = self.Logics(i, j, map, player, grid)
                if gain != [] and len(gain[0]) > 0:
                    return False
        return True

    def Possibiliter(self, n, m, map, player):
        possibiliter = []
        nx, mx = len(map), len(map[0])
        if 0 <= n < nx and 0 <= m < mx and map[n][m] == player.GetId():
            for i in range(n - 1, n + 2):
                for j in range(m - 1, m + 2):
                    if 0 <= i < nx and 0 <= j < mx and map[i][j] != player.GetAdversaire().GetId() and map[i][j] != player.GetId():
                        possibiliter.append([i, j])
        return possibiliter

class Node:
    def __init__(self, parent, data):
        self.parent = parent
        self.childs = []
        self.data = data

    def AddChild(self, child):
        if type(child) == Node:
            self.childs.append(child)

    def IsLeaf(self):
        if self.childs == []:
            return True
        return False

    def __eq__(self, other):
        return other.data == self.data

    def __gt__(self, other):
        return other.data < self.data

    def __lt__(self, other):
        return other.data > self.data

def PlusInfini():
    return 1000

def MoinInfini():
    return -1000

def Sauvegarder():
    pass

def Restaurer():
    pass

def FonctionEvaluation():
    pass

def MiniMax(node, profondeur, maximiser):
    if node.IsLeaf() or profondeur == 0:
        return FonctionEvaluation()

    if maximiser:
        max = None
        for child in node.childs:
            e = MiniMax(child, profondeur - 1, False)
            if max == None:
                max = e
            else:
                max = e if max < e else max

gameLogics = GameLogis()