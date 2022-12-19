class Person:
    def __init__(self):
        self.id = -1
        self.nickname = ""
        self.bio = ""
        self._role = -1
        self._power = ""
        self._zone = ""
        self.picture_url = ""

    def setId(self, id):
        self.id = id

    def setNickname(self, nickname):
        self.nickname = nickname

    def setRole(self, _role):
        self._role = _role

    def setBio(self, bio):
        self.bio = bio

    def setPower(self, _power):
        self._power = _power

    def setZone(self, _zone):
        self._zone = _zone

    def setPictureUrl(self, picture_url):
        self.picture_url = picture_url
    
    def getId(self):
        return self.id

    def getNickname(self):
        return self.nickname
    
    def getRole(self):
        return self._role

    def getBio(self):
        return self.bio

    def getPower(self):
        return self._power
    
    def getZone(self):
        return self._zone

    def getPictureUrl(self):
        return self.picture_url

    def getListAtributes(self):
        pass

    def show(self):
        pass