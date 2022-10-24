from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

from project.PersonList import PersonList

class BlogManager:

    bp = Blueprint('blog', __name__)

    @bp.route('/')

    def index():
        
        #personList = PersonList()

        #personList.addPerson('1', 'Daniel')

        db = DbManager.get_db()
        users = db.execute(
            'SELECT id, username'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()

        return render_template('blog/index.html', users = users)
        #return render_template('blog/index.html', users = personList.getPersonList())