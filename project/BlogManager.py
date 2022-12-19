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

    @AuthenticationManager.login_required
    @bp.route('/all')
    def all():

        list = BlogManager.personList.getPersonList()

        db = DbManager.get_db()

        users = db.execute(
            'SELECT id, username, id_person_id, tier'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()

        return render_template('blog/all.html', users = users, list = list)

    @AuthenticationManager.login_required
    @bp.route('/heroes')
    def heroes():

        list = BlogManager.personList.getPersonList()

        db = DbManager.get_db()

        users = db.execute(
            'SELECT id, username, id_person_id, tier'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()

        return render_template('blog/heroes.html', users = users, list = list)

    @AuthenticationManager.login_required
    @bp.route('/villains')
    def villains():
        list = BlogManager.personList.getPersonList()

        return render_template('blog/villains.html', list = list)

    @AuthenticationManager.login_required
    @bp.route('/create_villain', methods=('GET', 'POST'))
    def create_villain():
        if request.method == 'POST':

            nickname = request.form['nickname']
            _status = request.form['status']
            bio = request.form['bio']

            db = DbManager.get_db()
            error = None

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO person (nickname, _role, bio) VALUES (?, ?, ?)",
                        (nickname, 2, bio),
                    )
                    person = db.execute(
                                'SELECT * FROM person WHERE nickname = ?', (nickname,)
                            ).fetchone()
                    db.execute(
                        "INSERT INTO villain (_status, id_person_id) VALUES (?, ?)",
                        (_status, person['id']),
                    )

                    db.commit()
                except db.IntegrityError:
                    error = f"Villain {nickname} is already registered."
                else:
                    return redirect(url_for('index'))
            flash(error)

        return render_template('blog/create_villain.html')
