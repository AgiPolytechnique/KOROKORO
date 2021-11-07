from Background import Background
from Player import Human, IA, Grid
from Scene import Scene
from Widget import *
from Drawable import Drawable
from InputHandle import InputHandle
from Levels import Level


class MenuPrincipal(Scene):
    def __init__(self, game):
        super(MenuPrincipal, self).__init__(game, "MENU_PRINCIPAL")
        self.racio = [self.game.size[0], self.game.size[1]]

        self.background = Background("bg_mp")
        self.title = Background("titleKoro")
        self.nameMenu = Background("titleMenuPrincipal")
        self.copyright = Background("copyright")

        #bouton
        self.boutonHelp = Bouton(normal=["helpNormal", None], hover=["helpHover", None],
                                 deasable=["helpDeasable", None], pressed=["helpNormal", self.Help])
        self.boutonHelp.SetSize(428, 236)
        self.boutonHelp.SetScale(0.125, 0.125)
        self.boutonHelp.SetPosition(472, 391)

        self.boutonQuit = Bouton(normal=["quitNormal", None], hover=["quitHover", None],
                                 deasable=["quitDeasable", None], pressed=["quitNormal", self.Quit])
        self.boutonQuit.SetSize(408, 236)
        self.boutonQuit.SetScale(0.125, 0.125)
        self.boutonQuit.SetPosition(571, 391)

        self.boutonResume = Bouton(normal=["resumeNormal", None], hover=["resumeHover", None],
                                 deasable=["resumeDeasable", None], pressed=["resumeNormal", self.Resume])
        self.boutonResume.SetSize(716, 236)
        self.boutonResume.SetScale(0.125, 0.125)
        self.boutonResume.SetPosition(340, 391)
        self.boutonResume.SetDeasable()

        self.boutonNouveau = Bouton(normal=["nouveauNormal", None], hover=["nouveauHover", None],
                                 deasable=["nouveauDeasable", None], pressed=["nouveauNormal", self.NouveauJeu])
        self.boutonNouveau.SetSize(1489, 246)
        self.boutonNouveau.SetScale(0.125, 0.125)
        self.boutonNouveau.SetPosition(388, 344)

        self.nodes = []
        self.nodes.append(self.boutonHelp)
        self.nodes.append(self.boutonNouveau)
        self.nodes.append(self.boutonResume)
        self.nodes.append(self.boutonQuit)

    def EventInput(self, event):
        sx = 1
        sy = 1
        if event.type == VIDEORESIZE:
            '''sx = event.w / self.racio[0]
            sy = event.h / self.racio[1]
            for node in self.nodes:
                node.SetSize(node.transform.GetSize()[0] * sx, node.transform.GetSize()[1] * sy)
                node.SetPosition(node.transform.GetPosition()[0] * sx, node.transform.GetPosition()[1] * sy)
                #node.Scale(sx, sy, 0, 0)
            self.racio[0], self.racio[1] = event.w, event.h'''
            self.ScreenUpdate([event.w, event.h])
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.Quit()

        for node in self.nodes:
            if issubclass(type(node), InputHandle):
                node.EventInput(event)

    def ScreenUpdate(self, racio):
        sx = racio[0] / self.racio[0]
        sy = racio[1] / self.racio[1]
        for node in self.nodes:
            node.SetSize(node.transform.GetSize()[0] * sx, node.transform.GetSize()[1] * sy)
            node.SetPosition(node.transform.GetPosition()[0] * sx, node.transform.GetPosition()[1] * sy)
            # node.Scale(sx, sy, 0, 0)
        self.racio[0], self.racio[1] = racio[0], racio[1]

    def Update(self, dt):
        pass

    def Render(self):
        self.background.Render(self.game)
        self.title.Render(self.game)
        self.nameMenu.Render(self.game)
        self.copyright.Render(self.game)

        for node in self.nodes:
            if issubclass(type(node), Drawable):
                node.Render(self.game)

    def Quit(self):
        self.game.Close()

    def Help(self):
        pass

    def Resume(self):
        self.game.SetActiveScene("LEVEL")

    def NouveauJeu(self):
        self.boutonResume.SetDeasable(False)
        playerOne = Human(None)
        playerTwo = IA(playerOne)
        #playerTwo = Human(playerOne)
        playerOne.SetAdversair(playerTwo)
        playerOne.AddTexture("virusOrange")
        playerTwo.AddTexture("virusVert")
        grid = Grid()
        grid.AddTexture("carreauVerClaire")
        grid.AddTexture("carreauVerSombre")
        Level(self.game, playerOne, playerTwo, grid, self.racio)
        self.game.SetActiveScene("LEVEL")