import os

class Main:

    def __init__(self):
        print("Main executada")

        self.initializeFlask()

    def initializeFlask(self):
        flag = input("Qual o sistema operacional? [W]/[L] \n")

        if flag == 'W':
            os.system("py -m flask --app project init-db")
            os.system("py -m flask --app project --debug run")
        else:
            os.system("flask --app project init-db")
            os.system("flask --app project --debug run")

main = Main()