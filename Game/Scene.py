from Drawable import Drawable
from InputHandle import InputHandle


class Scene(Drawable, InputHandle):
    def __init__(self, game, name):
        self.game = game
        self.game.AddScene(name, self)

    def EventInput(self, event):
        pass

    def Update(self, dt):
        pass

    def Render(self):
        pass