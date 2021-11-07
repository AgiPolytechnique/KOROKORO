import pygame.image

class TextureManager():
    def __init__(self):
        self.__textures = {}

    def LoadFromFile(self, fileName):
        fichier = open(fileName, "r")

        while True:
            ligne = fichier.readline()
            if ligne != "":
                infos_copy = ligne.split("[[[*]]]")
                if len(infos_copy) == 2:
                    #print(infos_copy)
                    self.AddTexture(((infos_copy[1]).split("\n"))[0], infos_copy[0])
            else:
                break

    def AddTexture(self, fileName, name):
        if name in self.__textures:
            return False
        self.__textures[name] = pygame.image.load(fileName).convert_alpha()
        return True

    def GetTexture(self, name):
        if name in self.__textures:
            return self.__textures[name]
        return None

    def Rename(self, name, newName):
        if name in self.__textures:
            texture = self.__textures[name]
            if self.Remove(name):
                self.__textures[newName] = texture
                return True
        return False

    def Remove(self, name):
        if name in self.__textures:
            del self.__textures[name]
            return True
        return False

    def Clear(self):
        self.__textures.clear()

class AudioManager:
    def __init__(self):
        self.bruitages = {}
        self.musics = {}

    def LoadFromFile(self, fileName):
        fichier = open(fileName, "r")

        while True:
            ligne = fichier.readline()
            if ligne != "":
                infos_copy = ligne.split("[[[*]]]")
                if len(infos_copy) == 2:
                    #print(infos_copy)
                    self.Add(((infos_copy[1]).split("\n"))[0], infos_copy[0])
            else:
                break

    def Add(self, fileName, name, type="music"):
        if type == "music":
            if name in self.musics:
                return False
            self.musics[name] = pygame.mixer.Sound(fileName)
        elif type == "bruitage":
            if name in self.bruitages:
                return False
            self.bruitages[name] = pygame.mixer.Sound(fileName)
        return True

    def Get(self, name, type="music"):
        if type == "music":
            if name in self.musics:
                return self.musics[name]
        elif type == "bruitage":
            if name in self.bruitages:
                return self.bruitages[name]
        return None

    def Rename(self, name, newName, type="music"):
        if type == "music":
            if name in self.musics:
                music = self.musics[name]
                if self.Remove(name):
                    self.musics[newName] = music
                    return True
        elif type == "bruitage":
            if name in self.bruitages:
                music = self.bruitages[name]
                if self.Remove(name, "bruitage"):
                    self.bruitages[newName] = music
                    return True
        return False

    def Remove(self, name, type="music"):
        if type == "music":
            if name in self.musics:
                del self.musics[name]
                return True
        elif type == "bruitage":
            if name in self.bruitages:
                del self.bruitages[name]
                return True
        return False

    def Clear(self, type="music"):
        if type == "music":
            self.musics.clear()
        elif type == "bruitage":
            self.bruitages.clear()

textureManager = TextureManager()
audioManager = AudioManager()