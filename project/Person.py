from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import DbManager

class Person:
    def __init__(self):
        print("Pessoa Criada")

    def inicializar(self):
        self.nome = "Daniel"
        self.idade = 2

        print(self.nome + " tem " + str(self.idade) + " anos")

    