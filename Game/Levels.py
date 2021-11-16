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

        sx = self.racio[0] / self.game.size[0]
        sy = self.racio[1] / self.game.size[1]

        self.player_one = playerOne
        self.player_two = playerTwo
        self.human_and_ia = (issubclass(type(playerOne), Human) and issubclass(type(playerTwo), IA))\
                        or (issubclass(type(playerOne), Human) and issubclass(type(playerTwo), IA))
        self.grid = grid

        self.actualPlayer = self.player_one

        #self.background = Background("bg_bouche2")
        self.background = Background("bg_mp")
        self.player_view_one = [75, 20, 75*sx, 75*sy]
        self.player_view_title = [75, 20, 160*0.55*sx, 45*0.55*sy]
        self.player_view_nbc = [75, 20, 107*0.6*sx, 22*0.6*sy]
        self.player_view_score = [75, 20, 61*0.6*sx, 29*0.6*sy]
        self.view_virus_size = [45*sx, 45*sy]

        ligne = param["ligne"] if "ligne" in param else 7
        colone = param["colone"] if "colone" in param else 7

        self.size_grid_x = 56 * 7 * (sx) // ligne
        self.size_grid_y = 56 * 7 * (sy) // colone

        self.map = np.full(shape=(ligne,colone),fill_value=0 if self.grid == None else self.grid.GetId())

        self.scorePlayerOne = Text("0", 50, (255, 255, 255))
        self.scorePlayerTwo = Text("0", 50, (255, 255, 255))

        self.coupPlayerOne = Text("0", 25, (255, 255, 255))
        self.coupPlayerTwo = Text("0", 25, (255, 255, 255))

        self.winner_text = Text("", 25, (255, 255, 255))

        self.scorePlayerOne.SetScale2(sx, sy)
        self.scorePlayerTwo.SetScale2(sx, sy)

        self.coupPlayerOne.SetScale2(sx, sy)
        self.coupPlayerTwo.SetScale2(sx, sy)

        self.winner_text.SetScale2(sx, sy)

        self.isFinish = False

        if self.player_one != None:
            self.map[0][0] = self.map[ligne - 1][colone - 1] = self.player_one.GetId()
            self.player_one.AddPossibilityArray([[0, 1], [1, 0], [1, 1],
                                                 [ligne - 2, colone - 2], [ligne - 1, colone - 2],
                                                 [ligne - 2, colone - 1]])
            self.player_one.quantiter = 2
            self.scorePlayerOne.SetText(f"{self.player_one.quantiter}")
        if self.player_two != None:
            self.map[0][colone - 1] = self.map[ligne - 1][0] = self.player_two.GetId()
            self.player_two.AddPossibilityArray([[0, colone-2], [1, colone-2], [1, colone-1],
                                                 [ligne - 2, 0], [ligne - 1, 1],
                                                 [ligne - 2, 1]])
            self.player_two.quantiter = 2
            self.scorePlayerTwo.SetText(f"{self.player_one.quantiter}")

        self.gridPosition = [(self.racio[0] - ligne * self.size_grid_x)/2, (self.racio[1] - colone * self.size_grid_y)/2]

        self.sound_game_over = pygame.mixer.Sound('data/audio/bruitage/game_over.mp3')
        self.sound_game_win = pygame.mixer.Sound('data/audio/bruitage/game_win.mp3')
        self.sound_game_not_validate = pygame.mixer.Sound('data/audio/bruitage/jeu_non_valide.mp3')
        self.sound_game_tchop = pygame.mixer.Sound('data/audio/bruitage/manger.mp3')

        self.next_player = False

        self.Avantage()

        self.play_position = [None, None]

        #self.ScreenUpdate([racio[0], racio[1]])

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
                    j = (event.pos[0] - self.gridPosition[0])//self.size_grid_x
                    i = (event.pos[1] - self.gridPosition[1])//self.size_grid_y
                    self.Play(i, j)
                    self.next_player = True
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
        if gameLogics.GameFinish(self.map, self.actualPlayer, self.grid):
            pygame.mixer.music.stop()
            self.isFinish = True
            self.SetWinner()

            if self.human_and_ia:
                if issubclass(type(self.actualPlayer), Human):
                    win = self.actualPlayer.quantiter >= self.actualPlayer.GetAdversaire().quantiter
                else:
                    win = self.actualPlayer.quantiter <= self.actualPlayer.GetAdversaire().quantiter

                if win:
                    self.sound_game_win.play()
                else:
                    self.sound_game_over.play()
            pygame.mixer.music.play()
        else:
            self.Avantage()

    def Avantage(self):
        if self.player_one.quantiter > self.player_two.quantiter:
            self.winner_text.SetText("Avantage Joueur Un (1)")
        elif self.player_one.quantiter == self.player_two.quantiter:
            self.winner_text.SetText("Egaliter")
        else:
            self.winner_text.SetText("Avantage Joueur Deux (2)")

    def SetWinner(self):
        if self.player_one.quantiter > self.player_two.quantiter:
            self.winner_text.SetText("Joueur Un (1) Gagne")
        elif self.player_one.quantiter == self.player_two.quantiter:
            if len(self.player_one.possibiliter) > len(self.player_two.possibiliter):
                self.winner_text.SetText("Joueur Un (1) Gagne")
            elif len(self.player_one.possibiliter) < len(self.player_two.possibiliter):
                self.winner_text.SetText("Joueur Deux (2) Gagne")
            else:
                self.winner_text.SetText("Egaliter")
        else:
            self.winner_text.SetText("Joueur Deux (2) Gagne")

    def Play(self, i, j):
        self.play_position = [i, j]
        gain = gameLogics.Logics(int(i), int(j), self.map, self.actualPlayer, self.grid)

        if gain != [] and len(gain[0]) > 0:
            if len(gain[0]) - 1 > 0:
                self.sound_game_tchop.play()
            for g in gain[0]:
                self.map[g[0]][g[1]] = self.actualPlayer.GetId()
            retirer = []
            for p in gain[1]:
                if p in self.actualPlayer.GetAdversaire().possibiliter:
                    r = True
                    for i in range(p[0] - 1, p[0] + 2):
                        for j in range(p[1] - 1, p[1] + 2):
                            if 0 <= i < len(self.map) and 0 <= j < len(self.map[0]):
                                if self.map[i][j] == self.actualPlayer.GetAdversaire().GetId():
                                    r = False
                                    break
                    if r and not (p in retirer):
                        retirer.append(p)

            self.actualPlayer.quantiter += len(gain[0])
            self.actualPlayer.AddPossibilityArray(gain[1])
            self.actualPlayer.RemovePossibilityArray(gain[0])

            self.actualPlayer.GetAdversaire().quantiter -= (len(gain[0]) - 1)
            self.actualPlayer.GetAdversaire().RemovePossibilityArray(retirer)

            self.Possibiliter()
            self.Score()
            self.GameFinish()
            self.actualPlayer = self.actualPlayer.GetAdversaire()
        else:
            if self.isFinish == False:
                self.sound_game_not_validate.play()

    def Update(self, dt):
        if self.isFinish == False:
            if issubclass(type(self.actualPlayer), IA) and self.next_player != True:
                if self.actualPlayer.flex_state == "begin":
                    self.actualPlayer.Play(self.map, self.grid)
                elif self.actualPlayer.flex_state == "finish":
                    self.actualPlayer.flex_state = "begin"
                    time.sleep(1)
                    if self.actualPlayer.playPosition != [None, None]:
                        self.Play(int(self.actualPlayer.playPosition[0]), int(self.actualPlayer.playPosition[1]))
                    else:
                        self.Score()
                        self.GameFinish()
    def Score(self):
        if self.actualPlayer.GetId() == self.player_one.GetId():
            self.scorePlayerOne.SetText(f"{self.actualPlayer.quantiter}")
            self.scorePlayerTwo.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")
        elif self.actualPlayer.GetId() == self.player_two.GetId():
            self.scorePlayerTwo.SetText(f"{self.actualPlayer.quantiter}")
            self.scorePlayerOne.SetText(f"{self.actualPlayer.GetAdversaire().quantiter}")

    def Possibiliter(self):
        if self.actualPlayer.GetId() == self.player_one.GetId():
            self.coupPlayerOne.SetText(f"{len(self.actualPlayer.possibiliter)}")
            self.coupPlayerTwo.SetText(f"{len(self.actualPlayer.GetAdversaire().possibiliter)}")
        elif self.actualPlayer.GetId() == self.player_two.GetId():
            self.coupPlayerTwo.SetText(f"{len(self.actualPlayer.possibiliter)}")
            self.coupPlayerOne.SetText(f"{len(self.actualPlayer.GetAdversaire().possibiliter)}")

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

        x = (-self.winner_text.transform.size[0] + self.racio[0])/2
        hr = (self.racio[1] - self.size_grid_y*len(self.map[0]))/2
        y = self.racio[1] - ((hr - self.winner_text.transform.size[1])/2)
        self.winner_text.transform.SetPosition(x, y)
        self.winner_text.Render(self.game)

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

                if i == self.play_position[0]  and j == self.play_position[1]:
                    pygame.draw.rect(self.game.screen, (255, 255, 255),
                                     (xg + 1, yg + 1, self.size_grid_x - 2, self.size_grid_y - 2), 1)

        if self.next_player == True and issubclass(type(self.actualPlayer), IA):
            self.next_player = False