

class GameLogis:
    def Logics(self, n, m, map, player):
        gain = []
        nx, mx = len(map), len(map[0])
        #print(n, m)
        if 0<=n<nx and 0<=m<mx and map[n][m] != player.GetId() and map[n][m] != player.GetAdversaire().GetId():
            get_gain = False
            for i in range(n - 1, n + 2):
                for j in range(m - 1, m + 2):
                    if 0<=i<nx and 0<=j<mx:
                        if get_gain == False and map[i][j] == player.GetId():
                            get_gain = True
                        if map[i][j] == player.GetAdversaire().GetId():
                            gain.append([i, j])
            if get_gain == True:
                gain.append([n, m])
            else:
                gain = []
        return gain

    def Possibiliter(self, n, m, map, player):
        possibiliter = []
        nx, mx = len(map), len(map[0])
        if 0 <= n < nx and 0 <= m < mx and map[n][m] == player.GetId():
            for i in range(n - 1, n + 2):
                for j in range(m - 1, m + 2):
                    if 0 <= i < nx and 0 <= j < mx and map[i][j] != player.GetAdversaire().GetId() and map[i][j] != player.GetId():
                        possibiliter.append([i, j])
        return possibiliter

gameLogics = GameLogis()