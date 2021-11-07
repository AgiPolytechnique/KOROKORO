import numpy as np
import pygame
from pygame.locals import *
from Background import Background
from GameLogics import gameLogics
from Manager import textureManager
from Player import Human, IA
from Scene import Scene
from Widget import Text


class Level(Scene):
    def __init__(self, game, playerOne, playerTwo, grid, racio, **param):
        super(Level, self).__init__(game, "LEVEL")
        self.racio = racio

        self.player_one = playerOne
        self.player_two = playerTwo
        self.grid = grid

        self.actualPlayer = self.player_one

        #self.background = Background("bg_bouche")
        self.background = Background("bg_mp")

        ligne = param["ligne"] if "ligne" in param else 7
        colone = param["colone"] if "colone" in param else 7

        self.size_grid_x = 56 * 7 * (self.racio[0] / self.game.size[0]) // ligne
        self.size_grid_y = 56 * 7 * (self.racio[1] / self.game.size[1]) // colone

        self.map = np.full(shape=(ligne,colone),fill_value=0 if self.grid == None else self.grid.GetId())

        self.scorePlayerOne = Text("0", 50)
        self.scorePlayerTwo = Text("0", 50)

        if self.player_one != None:
            self.map[0][0] = self.map[ligne - 1][colone - 1] = self.player_one.GetId()
            if issubclass(type(self.player_one), IA):
                self.player_one.AddPossibiliter(0, 1)
                self.player_one.AddPossibiliter(1, 0)
                self.player_one.AddPossibiliter(1, 1)
                self.player_one.AddPossibiliter(ligne - 2, colone - 2)
                self.player_one.AddPossibiliter(ligne - 1, colone - 2)
                self.player_one.AddPossibiliter(ligne - 2, colone - 1)
            self.player_one.quantiter = 2
            self.scorePlayerOne.SetText(f"{self.player_one.quantiter}")
        if self.player_two != None:
            self.map[0][colone - 1] = self.map[ligne - 1][0] = self.player_two.GetId()
            self.player_two.quantiter = 2
            self.scorePlayerOne.SetText(f"{self.player_one.quantiter}")
            if issubclass(type(self.player_two), IA):
                self.player_two.AddPossibiliter(0, 1)
                self.player_two.AddPossibiliter(1, 0)
                self.player_two.AddPossibiliter(1, 1)
                self.player_two.AddPossibiliter(ligne - 2, colone - 2)
                self.player_two.AddPossibiliter(ligne - 1, colone - 2)
                self.player_two.AddPossibiliter(ligne - 2, colone - 1)

        self.gridPosition = [(self.racio[0] - ligne * self.size_grid_x)/2, (self.racio[1] - colone * self.size_grid_y)/2]

        self.scorePlayerOne.transform.SetPosition(self.gridPosition[0] - self.size_grid_x*10/3,
                                                  self.gridPosition[1] + self.size_grid_y*5/2)
        self.scorePlayerTwo.transform.SetPosition(self.gridPosition[0] + (self.size_grid_x + 1) * (len(self.map) + 2)
                                                  + self.size_grid_x/3,
                                                  self.gridPosition[1] + self.size_grid_y*5/2)

    def EventInput(self, event):
        if event.type == VIDEORESIZE:
            sx = event.w / self.racio[0]
            sy = event.h / self.racio[1]
            self.size_grid_x *= sx
            self.size_grid_y *= sy
            self.racio[0], self.racio[1] = event.w, event.h
            self.gridPosition = [(self.racio[0] - len(self.map) * self.size_grid_x) / 2,
                                 (self.racio[1] - len(self.map[0]) * self.size_grid_y) / 2]

            self.scorePlayerOne.SetScale(sx, sy)
            self.scorePlayerTwo.SetScale(sx, sy)

            self.scorePlayerOne.transform.SetPosition(self.gridPosition[0] - self.size_grid_x * 10 / 3,
                                                      self.gridPosition[1] + self.size_grid_y * 5 / 2)
            self.scorePlayerTwo.transform.SetPosition(
                self.gridPosition[0] + (self.size_grid_x + 1) * (len(self.map) + 2)
                + self.size_grid_x / 3,
                self.gridPosition[1] + self.size_grid_y * 5 / 2)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.game.GetScene("MENU_PRINCIPAL") != None:
                    self.game.GetScene("MENU_PRINCIPAL").ScreenUpdate(self.racio)
                    self.game.SetActiveScene("MENU_PRINCIPAL")

        if issubclass(type(self.actualPlayer), Human):
            if event.type == MOUSEBUTTONDOWN:
                i = (event.pos[0] - self.gridPosition[0])//self.size_grid_x
                j = (event.pos[1] - self.gridPosition[1])//self.size_grid_y

                gain = gameLogics.Logics(int(j), int(i), self.map, self.actualPlayer)

                if len(gain) > 0:
                    self.actualPlayer.AddQuantiter(len(gain))
                    print(self.actualPlayer.quantiter)
                    for g in gain:
                        self.map[g[0]][g[1]] = self.actualPlayer.GetId()
                    self.actualPlayer = self.actualPlayer.GetAdversaire()
                    self.actualPlayer.AddQuantiter(1-len(gain))

                    if self.actualPlayer.GetId() == self.player_one.GetId():
                        self.scorePlayerOne.SetText(f"{self.actualPlayer.quantiter}")
                        self.scorePlayerTwo.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")
                    else:
                        self.scorePlayerTwo.SetText(f"{self.actualPlayer.quantiter}")
                        self.scorePlayerOne.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")

    def Update(self, dt):
        if issubclass(type(self.actualPlayer), IA):
            if self.actualPlayer.flex_state == "begin":
                self.actualPlayer.Play(self.map)
            elif self.actualPlayer.flex_state == "finish":
                self.actualPlayer.flex_state = "begin"
                gain = gameLogics.Logics(int(self.actualPlayer.playPosition[0]), int(self.actualPlayer.playPosition[1]), self.map, self.actualPlayer)

                if len(gain) > 0:
                    self.actualPlayer.AddQuantiter(len(gain))
                    print(self.actualPlayer.quantiter)
                    for g in gain:
                        self.map[g[0]][g[1]] = self.actualPlayer.GetId()
                    print(self.map)
                    self.actualPlayer = self.actualPlayer.GetAdversaire()
                    self.actualPlayer.AddQuantiter(1 - len(gain))

                    if self.actualPlayer.GetId() == self.player_one.GetId():
                        self.scorePlayerOne.SetText(f"{self.actualPlayer.quantiter}")
                        self.scorePlayerTwo.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")
                    else:
                        self.scorePlayerTwo.SetText(f"{self.actualPlayer.quantiter}")
                        self.scorePlayerOne.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")



    def Render(self):
        self.background.Render(self.game)

        self.scorePlayerOne.Render(self.game)
        self.scorePlayerTwo.Render(self.game)

        paire = True if len(self.map) > 0 and len(self.map[0]) % 2 == 0 else False
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                xg = int(int(self.gridPosition[0]) + j * int(self.size_grid_x))
                yg = int(int(self.gridPosition[1]) + i * int(self.size_grid_y))

                if self.grid != None:
                    if (paire and (i % 2 == j % 2)) or ((paire == False) and (i % 2 != j % 2)):
                        self.grid.SetActiveTexture(0)
                    else:
                        self.grid.SetActiveTexture(1)
                    texture = textureManager.GetTexture(self.grid.GetActive())
                    texture = pygame.transform.smoothscale(texture, (int(self.size_grid_x), int(self.size_grid_y)))

                    self.game.screen.blit(texture, (xg, yg, self.size_grid_x, self.size_grid_y))

                player = None
                if self.map[i][j] == self.player_one.GetId():
                    player = self.player_one
                elif self.map[i][j] == self.player_two.GetId():
                    player = self.player_two

                if player != None:
                    texture = textureManager.GetTexture(player.GetActive())
                    texture = pygame.transform.smoothscale(texture, (int(self.size_grid_x - 4), int(self.size_grid_y - 4)))

                    self.game.screen.blit(texture, (xg + 2, yg + 2, self.size_grid_x, self.size_grid_y))