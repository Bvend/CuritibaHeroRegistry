from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

from project.Hero import Hero

from project.Villan import Villan

from project.Person import Person

class PersonList:

    def __init__(self):
        self.personList = []

    def updateDB(self):
        db = DbManager.get_db()

        self.personList = []

        list = db.execute(
            'SELECT *'
            ' FROM person '
            ' ORDER BY id'
        ).fetchall()

        for element in list:
            role = element['_role']
            id = element['id']

            if (role == 1):
                person = Hero()
                person.setTier(self.pesquisarTier(db, id))

            elif (role == 2):
                person = Villan()
                person.setStatus(self.pesquisarStatus(db,id))

            person.setId(id)
            person.setNickname(element['nickname'])
            person.setBio(element['bio'])
            person.setPower(element['_power'])
            person.setZone(element['_zone'])
            person.setRole(role)
            self.personList.append(person)

        return self.personList 

    def pesquisarTier(self, db, id):
        tiers = db.execute(
            ' SELECT id_person_id, tier'
            ' FROM user',
        ).fetchall()

        for tier in tiers:
            if tier['id_person_id'] == id:
                return tier['tier']
        return '-'
    
    def pesquisarStatus(self, db, id):
        status = db.execute(
            ' SELECT id_person_id, _status'
            ' FROM villain',
        ).fetchall()

        for s in status:
            if s['id_person_id'] == id:
                return s['_status']
        return "-"

    def addPerson(self, nickname, _role, bio):
        db = DbManager.get_db()
        try:
            db.execute(
                "INSERT INTO person (nickname, _role, bio) VALUES (?, ?, ?)",
                (nickname, _role, bio),
            )
            db.commit()
        except db.IntegrityError:
            print("Erro")
        
        self.personList = self.updateDB()
        self.printList()

    def getPersonList(self):
        self.personList = self.updateDB()
        return self.personList

