from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

from project.PersonList import PersonList
from project.AuthenticationManager import AuthenticationManager

class BlogManager:

    personList = PersonList()

    bp = Blueprint('blog', __name__)

    @bp.route('/')

    @AuthenticationManager.login_required
    def index():
        return render_template('blog/index.html')

    @bp.route('/home')
    def home():
        return render_template('blog/home.html')

    @bp.route('/all')
    def all():
        return render_template('blog/all.html')

    @bp.route('/heroes')
    def heroes():
        db = DbManager.get_db()

        users = db.execute(
            'SELECT id, username'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()

        #return render_template('blog/index.html', users = users)
        #return render_template('blog/index.html', users = personList.getPersonList())
        return render_template('blog/heroes.html', users = users)

    @bp.route('/villains')
    def villains():
        return render_template('blog/villains.html')
