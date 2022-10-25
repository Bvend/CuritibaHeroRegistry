from project.Person import Person

class Hero(Person):
    def __init__(self):
        super().__init__()
        self.tier = ''
        self.atributes = ["Tier: "]

    def setTier(self, tier):
        self.tier = tier

    def getListAtributes(self):
        return self.atributes

    def show(self, atribute):
        if atribute == "Tier: ":
            return self.tier