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
        #self.boutonHelp.SetDeasable(True)

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
        pygame.mixer.music.set_volume(0.1)
        self.game.GetScene("LEVEL").ScreenUpdate(self.racio)
        self.game.SetActiveScene("LEVEL")

    def NouveauJeu(self):
        if self.game.SetActiveScene("MENU_NEW_GAME") == None:
            MenuNewGame(self.game)
        self.game.GetScene("MENU_NEW_GAME").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_NEW_GAME")

class MenuNewGame(Scene):
    def __init__(self, game):
        super(MenuNewGame, self).__init__(game, "MENU_NEW_GAME")
        self.racio = [self.game.size[0], self.game.size[1]]

        self.background = Background("bg_mp")
        self.title = Background("titleKoro")
        self.copyright = Background("copyright")

        self.nouveauChoice = Bouton(normal=["gameNouveauChoice", None], hover=["gameNouveauChoice", None],
                                 deasable=["gameNouveauChoice", None], pressed=["gameNouveauChoice", None])
        self.nouveauChoice.SetSize(2182, 266)
        self.nouveauChoice.SetScale(0.125, 0.125)
        self.nouveauChoice.SetPosition((-self.nouveauChoice.GetSize()[0] + self.game.size[0])/2, 270)

        #bouton
        self.boutonSolo = Bouton(normal=["gameSolo", None], hover=["gameSoloHover", None],
                                 deasable=[None, None], pressed=["gameSoloHover", self.OnePlayer])
        self.boutonSolo.SetSize(897, 238)
        self.boutonSolo.SetScale(0.125, 0.125)
        self.boutonSolo.SetPosition((-self.boutonSolo.GetSize()[0] + self.game.size[0])/2, 350)

        self.boutonMulti = Bouton(normal=["gameMulti", None], hover=["gameMultiHover", None],
                                 deasable=[None, None], pressed=["gameMultiHover", self.TwoPlayer])
        self.boutonMulti.SetSize(1035, 236)
        self.boutonMulti.SetScale(0.125, 0.125)
        self.boutonMulti.SetPosition((-self.boutonMulti.GetSize()[0] + self.game.size[0])/2, 391)

        self.nodes = []
        self.nodes.append(self.boutonSolo)
        self.nodes.append(self.boutonMulti)
        self.nodes.append(self.nouveauChoice)

    def EventInput(self, event):
        sx = 1
        sy = 1
        if event.type == VIDEORESIZE:
            self.ScreenUpdate([event.w, event.h])
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.Previous()

        for node in self.nodes:
            if issubclass(type(node), InputHandle):
                #print(f"{node.transform.position} : {node.transform.size}")
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
        self.nouveauChoice.Render(self.game)
        self.copyright.Render(self.game)

        for node in self.nodes:
            if issubclass(type(node), Drawable):
                node.Render(self.game)

    def Previous(self):
        if self.game.SetActiveScene("MENU_PRINCIPAL") == None:
            MenuNewGame(self.game)
        self.game.GetScene("MENU_PRINCIPAL").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_PRINCIPAL")

    def OnePlayer(self):
        if self.game.SetActiveScene("MENU_DIFFICULTER") == None:
            self.game.RemoveScene("MENU_DIFFICULTER")
            playerOne = Human(None)
            playerTwo = IA(playerOne)
            playerOne.SetAdversair(playerTwo)
            MenuDifficulter(self.game, playerOne, playerTwo)
        self.game.GetScene("MENU_DIFFICULTER").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_DIFFICULTER")

    def TwoPlayer(self):
        if self.game.SetActiveScene("MENU_CHOIX_VIRUS") == None:
            self.game.RemoveScene("MENU_CHOIX_VIRUS")
            playerOne = Human(None)
            playerTwo = Human(playerOne)
            playerOne.SetAdversair(playerTwo)
            MenuChoixVirus(self.game, playerOne, playerTwo)
        self.game.GetScene("MENU_CHOIX_VIRUS").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_CHOIX_VIRUS")

class MenuDifficulter(Scene):
    def __init__(self, game, playerOne, playerTwo):
        super(MenuDifficulter, self).__init__(game, "MENU_DIFFICULTER")
        self.racio = [self.game.size[0], self.game.size[1]]

        self.playerOne = playerOne
        self.playerTwo = playerTwo

        self.background = Background("bg_mp")
        self.title = Background("titleKoro")
        self.copyright = Background("copyright")

        self.nouveauChoice = Bouton(normal=["gameDifficulter", None], hover=["gameDifficulter", None],
                                 deasable=["gameDifficulter", None], pressed=["gameDifficulter", None])
        self.nouveauChoice.SetSize(1216, 267)
        self.nouveauChoice.SetScale(0.125, 0.125)
        self.nouveauChoice.SetPosition((-self.nouveauChoice.GetSize()[0] + self.game.size[0])/2, 270)

        #bouton
        self.boutonFacile = Bouton(normal=["gameFacile", None], hover=["gameFacileHover", None],
                                 deasable=[None, None], pressed=["gameFacileHover", self.Facile])
        self.boutonFacile.SetSize(577, 246)
        self.boutonFacile.SetScale(0.125, 0.125)
        self.boutonFacile.SetPosition((-self.boutonFacile.GetSize()[0] + self.game.size[0])/2, 350 - 25)

        self.boutonMoyen = Bouton(normal=["gameMoyen", None], hover=["gameMoyenHover", None],
                                 deasable=[None, None], pressed=["gameMoyenHover", self.Moyen])
        self.boutonMoyen.SetSize(608, 236)
        self.boutonMoyen.SetScale(0.125, 0.125)
        self.boutonMoyen.SetPosition((-self.boutonMoyen.GetSize()[0] + self.game.size[0])/2, 391 - 25)
        #self.boutonMoyen.SetDeasable(True)

        self.boutonDifficile = Bouton(normal=["gameDifficile", None], hover=["gameDifficileHover", None],
                                 deasable=[None, None], pressed=["gameDifficileHover", self.Difficile])
        self.boutonDifficile.SetSize(769, 246)
        self.boutonDifficile.SetScale(0.125, 0.125)
        self.boutonDifficile.SetPosition((-self.boutonDifficile.GetSize()[0] + self.game.size[0])/2, 391 + 20)
        #self.boutonDifficile.SetDeasable(True)

        self.nodes = []
        self.nodes.append(self.boutonFacile)
        self.nodes.append(self.boutonMoyen)
        self.nodes.append(self.boutonDifficile)
        self.nodes.append(self.nouveauChoice)

    def EventInput(self, event):
        sx = 1
        sy = 1
        if event.type == VIDEORESIZE:
            self.ScreenUpdate([event.w, event.h])
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.Previous()

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
        self.nouveauChoice.Render(self.game)
        self.copyright.Render(self.game)

        for node in self.nodes:
            if issubclass(type(node), Drawable):
                node.Render(self.game)

    def Previous(self):
        self.game.GetScene("MENU_NEW_GAME").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_NEW_GAME")

    def Facile(self):
        self.Dif(0)

    def Moyen(self):
        self.Dif(2)

    def Difficile(self):
        self.Dif(4)

    def Dif(self, profondeur):
        if self.game.SetActiveScene("MENU_CHOIX_VIRUS") == None:
            self.game.RemoveScene("MENU_CHOIX_VIRUS")
            self.playerTwo.SetProfondeur(profondeur)
            MenuChoixVirus(self.game, self.playerOne, self.playerTwo)
        self.game.GetScene("MENU_CHOIX_VIRUS").ScreenUpdate(self.racio)
        self.game.SetActiveScene("MENU_CHOIX_VIRUS")

class MenuChoixVirus(Scene):
    def __init__(self, game, playerOne, playerTwo):
        super(MenuChoixVirus, self).__init__(game, "MENU_CHOIX_VIRUS")
        self.racio = [self.game.size[0], self.game.size[1]]
        self.playerOne = playerOne
        self.playerTwo = playerTwo

        self.background = Background("bg_mp")
        self.title = Background("titleKoro")
        self.copyright = Background("copyright")

        self.virusChoice = Bouton(normal=["gameVirus", None], hover=["gameVirus", None],
                                 deasable=["gameVirus", None], pressed=["gameVirus", None])
        self.virusChoice.SetSize(2032, 261)
        self.virusChoice.SetScale(0.125, 0.125)
        self.virusChoice.SetPosition((-self.virusChoice.GetSize()[0] + self.game.size[0])/2, 270)

        #bouton
        self.boutonVirus1 = Bouton(normal=["gameVirusBulbe", None], hover=["gameVirusBulbeHover", None],
                                 deasable=[None, None], pressed=["gameVirusBulbeHover", self.VirusBulbe])
        self.boutonVirus1.SetSize(704, 705)
        self.boutonVirus1.SetScale(0.125, 0.125)
        self.boutonVirus1.SetPosition((-self.boutonVirus1.GetSize()[0] + self.game.size[0])/2 - self.boutonVirus1.GetSize()[0], 350)

        self.boutonVirus2 = Bouton(normal=["gameVirusEtoile", None], hover=["gameVirusEtoileHover", None],
                                 deasable=[None, None], pressed=["gameVirusEtoileHover", self.VirusEtoile])
        self.boutonVirus2.SetSize(704, 705)
        self.boutonVirus2.SetScale(0.125, 0.125)
        self.boutonVirus2.SetPosition((-self.boutonVirus2.GetSize()[0] + self.game.size[0])/2 + self.boutonVirus2.GetSize()[0], 350)

        self.nodes = []
        self.nodes.append(self.boutonVirus1)
        self.nodes.append(self.boutonVirus2)
        self.nodes.append(self.virusChoice)

    def EventInput(self, event):
        sx = 1
        sy = 1
        if event.type == VIDEORESIZE:
            self.ScreenUpdate([event.w, event.h])
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.Previous()

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
        self.virusChoice.Render(self.game)
        self.copyright.Render(self.game)

        for node in self.nodes:
            if issubclass(type(node), Drawable):
                node.Render(self.game)

    def Previous(self):
        if issubclass(type(self.playerOne), IA):
            self.game.GetScene("MENU_DIFFICULTER").ScreenUpdate(self.racio)
            self.game.SetActiveScene("MENU_DIFFICULTER")
        else:
            self.game.GetScene("MENU_NEW_GAME").ScreenUpdate(self.racio)
            self.game.SetActiveScene("MENU_NEW_GAME")

    def VirusBulbe(self):
        self.Virus("virusVert", "virusOrange")

    def VirusEtoile(self):
        self.Virus("virusOrange", "virusVert")

    def Virus(self, virusOne, virusTwo):
        self.game.GetScene("MENU_PRINCIPAL").boutonResume.SetDeasable(False)
        pygame.mixer.music.set_volume(0.1)
        if self.game.SetActiveScene("LEVEL") == None:
            self.game.RemoveScene("LEVEL")
            self.playerTwo.AddTexture(virusTwo)
            self.playerOne.AddTexture(virusOne)
            grid = Grid()
            grid.AddTexture("carreauVerSombre")
            grid.AddTexture("carreauVerClaire")
            #grid.AddTexture("carreau_rouge_claire")
            #grid.AddTexture("carreau_rouge_sombre")
            Level(self.game, self.playerOne, self.playerTwo, grid, self.racio, ligne=9, colone=9)
        self.game.GetScene("LEVEL").ScreenUpdate(self.racio)
        self.game.SetActiveScene("LEVEL")