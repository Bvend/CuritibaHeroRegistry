from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

from project.PersonList import PersonList

from project.Person import Person

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
    @bp.route('/list/<type>')
    def list(type):

        list = BlogManager.personList.getPersonList()

        db = DbManager.get_db()

        users = db.execute(
            'SELECT id, username, id_person_id, tier'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()

        return render_template('blog/list.html', users = users, list = list, type = int(type))

    @AuthenticationManager.login_required
    @bp.route('/profile/<id>')
    def profile(id):
        person = Person()

        list = BlogManager.personList.getPersonList()

        for element in list:
            if (int(element.getId()) == int(id)):
                person = element

        return render_template('blog/profile.html', person = person)

    @AuthenticationManager.login_required
    @bp.route('/create_villain', methods=('GET', 'POST'))
    def create_villain():
        if request.method == 'POST':

            nickname = request.form['nickname']
            _status = request.form['status']
            bio = request.form['bio']
            _power = request.form['_power']
            _zone = request.form['_zone']
            picture_url = request.form['picture_url']
            _class = request.form['_class']


            db = DbManager.get_db()
            error = None

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO person (nickname, _role, bio, _power, _zone, picture_url, class) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (nickname, 2, bio, _power, _zone, picture_url, _class),
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

    @bp.route('/<int:id>/delete_person', methods=('POST',))
    @AuthenticationManager.login_required
    def delete_person(id):
        db = DbManager.get_db()

        data = db.execute(
             'SELECT is_adm, id FROM user WHERE id_person_id = ?', (id,),
        ).fetchone()
        condition = db.execute(
            'SELECT _role FROM person WHERE id = ?', (id,),
        ).fetchone()

        db.execute('DELETE FROM person WHERE id = ?', (id,))

        db.commit()

        if (condition['_role'] == 1):
            redirect(url_for('auth.delete', id= data['id']))
        
        return redirect(url_for('blog.index'))

