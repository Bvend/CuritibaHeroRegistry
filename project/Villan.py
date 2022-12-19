from project.Person import Person

class Villan(Person):
    def __init__(self):
        super().__init__()
        self._status = ""
        self.atributes = ["Status: "]

    def setStatus(self, _status):
        self._status = _status
    
    def getStatus(self):
        return self._status

    def getListAtributes(self):
        return self.atributes

    def show(self, atribute):
        if atribute == "Status: ":
            return self._status
        elif atribute == "Bio: ":
            return self.bio
        
        