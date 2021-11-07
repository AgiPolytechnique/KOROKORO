from Drawable import Drawable
from Manager import textureManager
import pygame


class Background(Drawable):
    def __init__(self, name):
        self.name = name

    def Render(self, game):
        size = game.screen.get_size()
        img = pygame.transform.smoothscale(textureManager.GetTexture(self.name), size)
        game.screen.blit(img, (0, 0, size[0], size[1]))