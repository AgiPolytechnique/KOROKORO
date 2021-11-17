import pygame
from pygame.locals import *

from Levels import Level
from Manager import textureManager
from Menu import MenuPrincipal


class Game:
    def __init__(self):
        self.Init()

    # initialisation du jeu
    def Init(self):
        self.running = True

        # init pygame
        pygame.init()

        # windows config
        self.flags = RESIZABLE
        self.size = [960, 540]
        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption('Korokoro')

        # scene
        self.scenes = {}
        self.scene = None

        # load texture
        textureManager.LoadFromFile("data/textures/textures.txt")
        pygame.display.set_icon(textureManager.GetTexture("icon_korokoro"))

        self.background_sound = pygame.mixer.music.load("data/audio/musics/AUD-20211108-WA0013.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        MenuPrincipal(self)

    # add scene
    def AddScene(self, name, scene):
        self.scenes[name] = scene
        self.scene = scene

    def SetActiveScene(self, name):
        if name in self.scenes:
            self.scene = self.scenes[name]

    def GetScene(self, name):
        if name in self.scenes:
            return self.scenes[name]
        return None

    def NewLevel(self, level):
        p1 = level.player_one
        p2 = level.player_two
        g = level.grid
        r = level.racio
        l = len(level.map)
        c = len(level.map[0])
        self.RemoveScene("LEVEL")
        Level(self, p1, p2, g, r, ligne=l, colone=c)
        #self.GetScene("LEVEL").ScreenUpdate(r)
        self.SetActiveScene("LEVEL")

    def RemoveScene(self, name):
        if name in self.scenes:
            actualise = False
            if self.scene == self.scenes[name]:
                actualise = True
            del self.scenes[name]

            if len(self.scenes) > 0:
                self.scene = None
            else:
                self.scene = None

    # boucle de jeu
    def Run(self):
        while self.running:
            # gestion des evenements de la scene actuel
            self.EventInput()

            # mise a jour de la scene actuel
            self.Update(0)

            # affichage de la scene actuel
            self.Render()

            pygame.display.update()

        self.Quit()

    def Close(self):
        self.running = False

    def EventInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:# or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.Close()
            if self.scene != None:
                self.scene.EventInput(event)

    def Update(self, dt):
        if self.scene != None:
            self.scene.Update(dt)

    def Render(self):
        if self.scene != None:
            self.scene.Render()

    # sorti du jeu
    def Quit(self):
        # quit pygame
        pygame.quit()