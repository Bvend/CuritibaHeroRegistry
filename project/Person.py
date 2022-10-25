class Person:
    def __init__(self):
        self.id = -1
        self.nickname = ""
        self._role = -1

    def setId(self, id):
        self.id = id

    def setNickname(self, nickname):
        self.nickname = nickname

    def setRole(self, _role):
        self._role = _role

    def getId(self):
        return self.id

    def getNickname(self):
        return self.nickname
    
    def getRole(self):
        return self._role

    def getListAtributes(self):
        pass

    def show(self):
        pass