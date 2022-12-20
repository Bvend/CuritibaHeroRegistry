class Person:
    def __init__(self):
        self.id = -1
        self.nickname = ""
        self.bio = ""
        self._role = -1
        self._power = ""
        self._zone = ""
        self._class = ""
        self.picture_url = ""
        self.birth_day = -1
        self.birth_month = -1
        self.birth_year = -1

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

    def setClass(self, _class):
        self._class = _class
    
    def setBirthDate(self, birth_day, birth_month, birth_year):
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year

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

    def getClass(self):
        return self._class

    def getBirthDay(self):
        return self.birth_day
    def getBirthMonth(self):
        return self.birth_month
    def getBirthYear(self):
        return self.birth_year

    def getListAtributes(self):
        pass

    def show(self):
        pass