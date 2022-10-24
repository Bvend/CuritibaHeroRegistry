import os

import Person

class Main:

    def __init__(self):
        print("Main executada")

        self.initializeFlask()

        self.createLists()

    def initializeFlask(self):
        flag = input("Qual o sistema operacional? [W]/[L] \n")

        if flag == 'W':
            os.system("py -m flask --app project init-db")
            os.system("py -m flask --app project --debug run")
        else:
            os.system("flask --app project init-db")
            os.system("flask --app project --debug run")

    def createLists(self):
        print("Criadas")
        #personList = PersonList.PersonList()

main = Main()