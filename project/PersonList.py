from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

class PersonList:
    
    def __init__(self):
        self.personList = self.updateDB()
    
    def updateDB(self):
        db = DbManager.get_db()

        personList = db.execute(
            'SELECT *'
            ' FROM person '
            ' ORDER BY id'
        ).fetchall()

        return personList 

    def addPerson(self, _role, nickname):
        db = DbManager.get_db()
        try:
            db.execute(
                "INSERT INTO person (nickname, _role) VALUES (?, ?)",
                (nickname, _role),
            )
            db.commit()
        except db.IntegrityError:
            print("Erro")
        
        self.personList = self.updateDB()
        self.printList()
    
    def printList(self):
        for person in self.personList:
            print((person['nickname']) + " " + str(person['_role']))

    def getPersonList(self):
        return self.personList

