import random


class GameLogis:
    def Logics(self, n, m, map, player, grid):
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

def PlusInfini():
    return 1000

def MoinInfini():
    return -1000

def FonctionEvaluation(joueur, node, map, grid):
    #return len(gameLogics.Logics(node[0], node[1], map, joueur, grid)[0])
    q1 = joueur.quantiter
    q2 = joueur.GetAdversaire().quantiter
    g = len(gameLogics.Logics(node[0], node[1], map, joueur, grid)[0])
    return q1 + g*2 - q2 - 1

def GamePlay(player, nodes, nodes_a, node, map, grid):
    valuation = gameLogics.Logics(node[0], node[1], map, player, grid)

    for g in valuation[0]:
        map[g[0]][g[1]] = player.GetId()

    player.quantiter += len(valuation[0])
    player.GetAdversaire().quantiter -= (len(valuation[0]) - 1)

    retirer = []
    for p in valuation[1]:
        if p in nodes_a:
            r = True
            for i in range(p[0] - 1, p[0] + 2):
                for j in range(p[1] - 1, p[1] + 2):
                    if 0 <= i < len(map) and 0 <= j < len(map[0]):
                        if map[i][j] == player.GetAdversaire().GetId():
                            r = False
                            break
            if r and not (p in retirer):
                retirer.append(p)

    nodes_new = nodes.copy()
    for n in valuation[1]:
        if not n in nodes_new:
            nodes_new.append(n)
    for n in valuation[0]:
        if n in nodes_new:
            nodes_new.remove(n)

    nodes_a_new = nodes_a.copy()
    for n in retirer:
        if n in nodes_a_new:
            nodes_a_new.remove(n)

    return nodes_new, nodes_a_new

def Gagner(joueur, map, nodes1, nodes2):
    return True if (len(nodes1) <= 0 or len(nodes2) <= 0 and
                    joueur.quantiter > joueur.GetAdversaire().quantiter) else False

def Perdu(joueur, map, nodes1, nodes2):
    return True if (len(nodes1) <= 0 or len(nodes2) <= 0 and
                    joueur.quantiter < joueur.GetAdversaire().quantiter) else False

def MatchNulle(joueur, map, nodes1, nodes2):
    return True if (len(nodes1) <= 0 or len(nodes2) <= 0 and
                    joueur.quantiter == joueur.GetAdversaire().quantiter) else False

def MiniMaxi(joueur, nodes, nodes_a, node, map, profondeur, maximisation, grid):
    if Gagner(joueur, map, nodes, nodes_a):
        return PlusInfini()
    if Perdu(joueur, map, nodes, nodes_a):
        return MoinInfini()
    if MatchNulle(joueur, map, nodes, nodes_a):
        return 0

    if profondeur == 0:
        return FonctionEvaluation(joueur, node, map, grid)

    evaluation = MoinInfini() if maximisation else PlusInfini()
    map_copy = map.copy()

    quantiter_une = joueur.quantiter
    quantiter_deux = joueur.GetAdversaire().quantiter

    nodes_, nodes_a_ = GamePlay(joueur, nodes, nodes_a, node, map_copy, grid)

    for node in nodes_a_:
        e = MiniMaxi(joueur.GetAdversaire(), nodes_a_, nodes_, node, map_copy, profondeur-1, not maximisation, grid)
        if maximisation:
            evaluation = e if e > evaluation else evaluation
        else:
            evaluation = e if e < evaluation else evaluation

    joueur.quantiter = quantiter_une
    joueur.GetAdversaire().quantiter = quantiter_deux

    return evaluation

def DecisionMiniMax(map, player, profondeur, grid):
    maximisation = MoinInfini()
    node_end = [None, None]
    nodes = player.possibiliter
    nodes_a = player.GetAdversaire().possibiliter

    for node in nodes:
        evaluation = MiniMaxi(player, nodes, nodes_a, node, map.copy(), profondeur, False, grid)
        if evaluation > maximisation:
            maximisation = evaluation
            node_end = node
        elif evaluation == maximisation and random.randint(0, 1) == 0:
            node_end = node

    return node_end

def AlphaBeta(node, nodes, nodes_a, player, alpha, beta, maximisation, profondeur, map, grid):
    if Gagner(player, map, nodes, nodes_a):
        return PlusInfini()
    if Perdu(player, map, nodes, nodes_a):
        return MoinInfini()
    if MatchNulle(player, map, nodes, nodes_a):
        return 0

    if profondeur == 0:
        return FonctionEvaluation(player, node, map, grid)

    alpha_, beta_ = alpha, beta

    map_copy = map.copy()

    quantiter_une = player.quantiter
    quantiter_deux = player.GetAdversaire().quantiter

    nodes_, nodes_a_ = GamePlay(player, nodes, nodes_a, node, map_copy, grid)

    if maximisation:
        max = MoinInfini()
        for node in nodes_a_:
            a = AlphaBeta(node, nodes_a_, nodes_, player.GetAdversaire(), alpha_, beta_,
                          not maximisation, profondeur-1, map_copy, grid)

            if a > max:
                max = a
            if max >= beta_:
                player.quantiter = quantiter_une
                player.GetAdversaire().quantiter = quantiter_deux
                return max
            if max > alpha_:
                alpha_ = max
        player.quantiter = quantiter_une
        player.GetAdversaire().quantiter = quantiter_deux
        return alpha_
    else:
        min = PlusInfini()
        for node in nodes_a_:
            b = AlphaBeta(node, nodes_a_, nodes_, player.GetAdversaire(), alpha_, beta_,
                          not maximisation, profondeur-1, map_copy, grid)

            if b < min:
                min = b
            if alpha_ >= min:
                player.quantiter = quantiter_une
                player.GetAdversaire().quantiter = quantiter_deux
                return min
            if min < beta_:
                beta_ = min
        player.quantiter = quantiter_une
        player.GetAdversaire().quantiter = quantiter_deux
        return beta_

def DecisionAlphaBeta(map, player, profondeur, grid):
    alpha = MoinInfini()

    node_end = [None, None]
    nodes = player.possibiliter
    nodes_a = player.GetAdversaire().possibiliter

    for node in nodes:
        evaluation = AlphaBeta(node, nodes, nodes_a, player, alpha, PlusInfini(), False, profondeur, map, grid)
        if evaluation > alpha:
            alpha = evaluation
            node_end = node
        elif evaluation == alpha and random.randint(0, 1) == 0:
            node_end = node

    return node_end

gameLogics = GameLogis()