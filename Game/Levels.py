import time

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
        self.racio = [racio[0], racio[1]]

        self.player_one = playerOne
        self.player_two = playerTwo
        self.grid = grid

        self.actualPlayer = self.player_one

        #self.background = Background("bg_bouche2")
        self.background = Background("bg_mp")
        self.player_view_one = [75, 20, 75, 75]
        self.player_view_title = [75, 20, 160*0.55, 45*0.55]
        self.player_view_nbc = [75, 20, 107*0.6, 22*0.6]
        self.player_view_score = [75, 20, 61*0.6, 29*0.6]
        self.view_virus_size = [45, 45]

        ligne = param["ligne"] if "ligne" in param else 7
        colone = param["colone"] if "colone" in param else 7

        self.size_grid_x = 56 * 7 * (self.racio[0] / self.game.size[0]) // ligne
        self.size_grid_y = 56 * 7 * (self.racio[1] / self.game.size[1]) // colone

        self.map = np.full(shape=(ligne,colone),fill_value=0 if self.grid == None else self.grid.GetId())

        self.scorePlayerOne = Text("0", 50, (255, 255, 255))
        self.scorePlayerTwo = Text("0", 50, (255, 255, 255))

        self.coupPlayerOne = Text("0", 25, (255, 255, 255))
        self.coupPlayerTwo = Text("0", 25, (255, 255, 255))

        self.isFinish = False

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
            self.scorePlayerTwo.SetText(f"{self.player_one.quantiter}")
            if issubclass(type(self.player_two), IA):
                self.player_two.AddPossibiliter(0, 1)
                self.player_two.AddPossibiliter(1, 0)
                self.player_two.AddPossibiliter(1, 1)
                self.player_two.AddPossibiliter(ligne - 2, colone - 2)
                self.player_two.AddPossibiliter(ligne - 1, colone - 2)
                self.player_two.AddPossibiliter(ligne - 2, colone - 1)

        self.gridPosition = [(self.racio[0] - ligne * self.size_grid_x)/2, (self.racio[1] - colone * self.size_grid_y)/2]

        self.sound_game_over = pygame.mixer.Sound('data/audio/bruitage/game_over.mp3')
        self.sound_game_win = pygame.mixer.Sound('data/audio/bruitage/game_win.mp3')
        self.sound_game_not_validate = pygame.mixer.Sound('data/audio/bruitage/jeu_non_valide.mp3')
        self.sound_game_tchop = pygame.mixer.Sound('data/audio/bruitage/manger.mp3')

    def EventInput(self, event):
        if event.type == VIDEORESIZE:
            self.ScreenUpdate([event.w, event.h])

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.game.GetScene("MENU_PRINCIPAL") != None:
                    pygame.mixer.music.set_volume(0.3)
                    self.game.GetScene("MENU_PRINCIPAL").ScreenUpdate(self.racio)
                    self.game.SetActiveScene("MENU_PRINCIPAL")

        if self.isFinish == False:
            if issubclass(type(self.actualPlayer), Human):
                if event.type == MOUSEBUTTONDOWN:
                    i = (event.pos[0] - self.gridPosition[0])//self.size_grid_x
                    j = (event.pos[1] - self.gridPosition[1])//self.size_grid_y

                    gain = gameLogics.Logics(int(j), int(i), self.map, self.actualPlayer)

                    self.actualPlayer.nom_coup += 1
                    if self.actualPlayer.GetId() == self.player_one.GetId():
                        self.coupPlayerOne.SetText(f"{self.actualPlayer.nom_coup}")
                    elif self.actualPlayer.GetId() == self.player_two.GetId():
                        self.coupPlayerTwo.SetText(f"{self.actualPlayer.nom_coup}")

                    if len(gain) > 0:
                        if len(gain) - 1 > 0:
                            self.sound_game_tchop.play()
                        #print(self.actualPlayer.quantiter)
                        for g in gain:
                            self.map[g[0]][g[1]] = self.actualPlayer.GetId()

                        self.actualPlayer.AddQuantiter(len(gain))
                        self.actualPlayer.GetAdversaire().AddQuantiter(1 - len(gain))

                        self.scorePlayerOne.SetText(f"{self.player_one.quantiter}")
                        self.scorePlayerTwo.SetText(f"{self.player_two.quantiter}")

                        #print(f"{self.player_one.quantiter}",f"{self.player_two.quantiter}")

                        self.actualPlayer = self.actualPlayer.GetAdversaire()

                        self.GameFinish()
                    else:
                        if self.isFinish == False:
                            self.sound_game_not_validate.play()
        else:
            if event.type == KEYDOWN:
                if event.key == K_r:
                    self.player_one.Reset()
                    self.player_two.Reset()
                    self.game.NewLevel(self)

    def ScreenUpdate(self, racio):
        sx = racio[0] / self.racio[0]
        sy = racio[1] / self.racio[1]
        self.size_grid_x *= sx
        self.size_grid_y *= sy
        self.racio[0], self.racio[1] = racio[0], racio[1]
        self.gridPosition = [(self.racio[0] - len(self.map) * self.size_grid_x) / 2,
                             (self.racio[1] - len(self.map[0]) * self.size_grid_y) / 2]

        self.player_view_one[0] *= sx
        self.player_view_one[1] *= sy
        self.player_view_one[2] *= sx
        self.player_view_one[3] *= sy

        self.player_view_title[2] *= sx
        self.player_view_title[3] *= sy

        self.player_view_nbc[2] *= sx
        self.player_view_nbc[3] *= sy

        self.player_view_score[2] *= sx
        self.player_view_score[3] *= sy

        self.view_virus_size[0] *= sx
        self.view_virus_size[1] *= sy

        self.scorePlayerOne.SetScale2(sx, sy)
        self.scorePlayerTwo.SetScale2(sx, sy)

        self.coupPlayerOne.SetScale2(sx, sy)
        self.coupPlayerTwo.SetScale2(sx, sy)

    def GameFinish(self):
        if gameLogics.GameFinish(self.map, self.actualPlayer):
            pygame.mixer.music.stop()
            self.isFinish = True
            if issubclass(type(self.actualPlayer), Human) and issubclass(type(self.actualPlayer.GetAdversaire()), IA):
                self.sound_game_over.play()
            elif issubclass(type(self.actualPlayer), IA) and issubclass(type(self.actualPlayer.GetAdversaire()), Human):
                self.sound_game_win.play()
            pygame.mixer.music.play()

    def Update(self, dt):
        if self.isFinish == False:
            if issubclass(type(self.actualPlayer), IA):
                if self.actualPlayer.flex_state == "begin":
                    self.actualPlayer.Play(self.map)
                elif self.actualPlayer.flex_state == "finish":
                    self.actualPlayer.flex_state = "begin"
                    gain = gameLogics.Logics(int(self.actualPlayer.playPosition[0]), int(self.actualPlayer.playPosition[1]), self.map, self.actualPlayer)

                    self.actualPlayer.nom_coup += 1
                    if self.actualPlayer.GetId() == self.player_one.GetId():
                        self.coupPlayerOne.SetText(f"{self.actualPlayer.nom_coup}")
                    elif self.actualPlayer.GetId() == self.player_two.GetId():
                        self.coupPlayerTwo.SetText(f"{self.actualPlayer.nom_coup}")

                    if len(gain) > 0:
                        if len(gain) - 1 > 0:
                            self.sound_game_tchop.play()
                        self.actualPlayer.AddQuantiter(len(gain))
                        #print(self.actualPlayer.quantiter)
                        for g in gain:
                            self.map[g[0]][g[1]] = self.actualPlayer.GetId()
                        time.sleep(1)
                        self.actualPlayer = self.actualPlayer.GetAdversaire()
                        self.actualPlayer.AddQuantiter(1 - len(gain))

                        self.GameFinish()

                        if self.actualPlayer.GetId() == self.player_one.GetId():
                            self.scorePlayerOne.SetText(f"{self.actualPlayer.quantiter}")
                            self.scorePlayerTwo.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")
                        elif self.actualPlayer.GetId() == self.player_two.GetId():
                            self.scorePlayerTwo.SetText(f"{self.actualPlayer.quantiter}")
                            self.scorePlayerOne.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")
                    else:
                        if self.isFinish == False:
                            self.sound_game_not_validate.play()

    def Render(self):
        self.background.Render(self.game)

        x, y, w, h = self.player_view_one[0], self.player_view_one[1], self.player_view_one[3], self.player_view_one[3]
        x1, y1, w1, h1 = self.player_view_title[0], self.player_view_title[1], self.player_view_title[2], self.player_view_title[3]
        w2, h2 = self.view_virus_size[0], self.view_virus_size[1]
        w3, h3 = self.player_view_nbc[2], self.player_view_nbc[3]
        w4, h4 = self.player_view_score[2], self.player_view_score[3]

        texture_circle = pygame.transform.smoothscale(textureManager.GetTexture("playerCircle"), (int(w), int(h)))
        texture_v1 = pygame.transform.smoothscale(textureManager.GetTexture(self.player_one.GetItem(0)), (int(w2), int(h2)))
        texture_v2 = pygame.transform.smoothscale(textureManager.GetTexture(self.player_two.GetItem(0)), (int(w2), int(h2)))
        texture_pt_o = pygame.transform.smoothscale(textureManager.GetTexture("playerOneTitle"), (int(w1), int(h1)))
        texture_pt_t = pygame.transform.smoothscale(textureManager.GetTexture("playerTwoTitle"), (int(w1), int(h1)))
        texture_nbrc = pygame.transform.smoothscale(textureManager.GetTexture("Nbredecoups"), (int(w3), int(h3)))
        texture_score = pygame.transform.smoothscale(textureManager.GetTexture("Score"), (int(w4), int(h4)))

        if self.actualPlayer.GetId() == self.player_one.GetId():
            pygame.draw.ellipse(self.game.screen, (0, 255, 64, 100), (x + (w - 10)/2, y + h - 10, 10, 10))
        elif self.actualPlayer.GetId() == self.player_two.GetId():
            pygame.draw.ellipse(self.game.screen, (0, 255, 64, 100), (self.racio[0] - x - w + (w - 10)/2, y + h - 10, 10, 10))

        self.game.screen.blit(texture_circle, (x, y, w, h))
        self.game.screen.blit(texture_v1, (x+(w - w2)/2, y+(h - h2)/2, w, h))
        self.game.screen.blit(texture_pt_o, (x + w + 20, y, w1, h1))
        self.game.screen.blit(texture_nbrc, (x + w + 20, y + h1 + 20, w3, h3))
        self.game.screen.blit(texture_score, (x + w + 20, y + h1 + h3 + 30, w4, h4))
        pygame.draw.line(self.game.screen, (255, 255, 255), (x + w + 20, y + h1 + 10), (x + w + 20 + w1, y + h1 + 10), 1)

        self.scorePlayerOne.transform.SetPosition(x + w + 20 + w4 + 10, y + h1 + h3 + 30)
        self.scorePlayerOne.Render(self.game)

        self.coupPlayerOne.transform.SetPosition(x + w + 20 + w3 + 10, y + h1 + 20)
        self.coupPlayerOne.Render(self.game)

        self.game.screen.blit(texture_circle, (self.racio[0] - x - w, y, w, h))
        self.game.screen.blit(texture_v2, (self.racio[0] - x - w + (w - w2)/2, y + (h - h2)/2, w, h))
        self.game.screen.blit(texture_pt_t, (self.racio[0] - x - w - w1 - 20, y, w1, h1))
        self.game.screen.blit(texture_nbrc, (self.racio[0] - x - w - w1 - 20, y + h1 + 20, w3, h3))
        self.game.screen.blit(texture_score, (self.racio[0] - x - w - w1 - 20, y + h1 + h3 + 30, w4, h4))
        pygame.draw.line(self.game.screen, (255, 255, 255), (self.racio[0] - x - w - w1 - 20, y + h1 + 10),
                                                    (self.racio[0] - x - w - w1 - 20 + w1, y + h1 + 10),1)

        self.scorePlayerTwo.transform.SetPosition(self.racio[0] - x - w - w1 - 20 + w4 + 10, y + h1 + h3 + 30)
        self.scorePlayerTwo.Render(self.game)

        self.coupPlayerTwo.transform.SetPosition(self.racio[0] - x - w - w1 - 20 + w3 + 10, y + h1 + 20)
        self.coupPlayerTwo.Render(self.game)

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