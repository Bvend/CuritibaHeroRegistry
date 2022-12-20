from project.Person import Person

class Hero(Person):
    def __init__(self):
        super().__init__()
        self.tier = ''
        self.atributes = ["Tier: "]
        self.isadm = 0

    def setAdm(self, isadm):
        self.isadm = isadm

    def setTier(self, tier):
        self.tier = tier

    def getListAtributes(self):
        return self.atributes

    def getAdm(self):
        return self.isadm

    def show(self, atribute):
        if atribute == "Tier: ":
            return self.tier
        if atribute == "Eh adm: ":
            return self.isadm