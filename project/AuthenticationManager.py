import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from project.DbManager import DbManager

from project.Person import Person

from project.PersonList import PersonList

from datetime import date

class AuthenticationManager:

    bp = Blueprint('auth', __name__, url_prefix='/auth')

    @bp.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            captcha = request.form['captcha']

            nickname = request.form['nickname']
            tier = request.form['tier']
            bio = request.form['bio']
            _power = request.form['_power']
            _zone = request.form['_zone']
            picture_url = request.form['picture_url']

            _date = request.form['date'].split('-')
            _date = date(int(_date[0]), int(_date[1]), int(_date[2]))

            db = DbManager.get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not captcha:
                error = 'Captcha is required'
            elif not captcha:
                error = 'Captcha is required'
            elif not bio:
                error = 'Bio is required'

            if error is None:
                try:
                    db.execute(
                        'INSERT INTO person '
                        '(nickname, _role, bio, _power, _zone, picture_url, birth_day, birth_month, birth_year) '
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (nickname, 1, bio, _power, _zone, picture_url, _date.day, _date.month, _date.year),
                    )
                    person = db.execute(
                                'SELECT * FROM person'
                            ).fetchall()
                    db.execute(
                        "INSERT INTO user (username, password, id_person_id, tier, is_adm) VALUES (?, ?, ?, ?, ?)",
                        (username, generate_password_hash(password), person[-1]['id'], tier, 0),
                    )
                    if (person[-1]['id'] == 1):
                        db.execute(
                            'UPDATE user SET is_adm = 1 WHERE username = ?', (username,)
                        )
                    
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    session.clear()
                    user = db.execute(
                                'SELECT * FROM user WHERE username = ?', (username,)
                            ).fetchone()
                    session['user_id'] = user['id']
                    return redirect(url_for('index'))

            flash(error)

        return render_template('auth/register.html')

    @bp.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = DbManager.get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

        return render_template('auth/login.html')

    @bp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = DbManager.get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

    @bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('blog.home'))

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('blog.home'))

            return view(**kwargs)
        return wrapped_view

    @bp.route('/<int:id>/update', methods=('GET', 'POST'))
    @login_required
    def update(id):
        person = Person()
        db = DbManager.get_db()
        data = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()
        personList = PersonList()
        personList.getPersonList()
        print(data['id_person_id'])
        person = personList.searchById(int(data['id_person_id']))

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            nickname = request.form['nickname']
            tier = request.form['tier']
            bio = request.form['bio']
            _power = request.form['_power']
            _zone = request.form['_zone']
            picture_url = request.form['picture_url']

            _date = request.form['date'].split('-')
            _date = date(int(_date[0]), int(_date[1]), int(_date[2]))
            error = None
            
            if not username:
                error = 'Username is required.'

            if error is not None:
                flash(error)
            else:
                db = DbManager.get_db()

                db.execute(
                    'UPDATE user SET username = ?, password= ?, tier = ?'
                    ' WHERE id = ?',
                    (username, generate_password_hash(password), tier, id)
                )

                data = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()

                db.execute(
                    'UPDATE person '
                    ' SET nickname = ?, bio = ?, _power = ?, _zone = ?, picture_url = ?,'
                    ' birth_day = ?, birth_month = ?, birth_year = ?'
                    ' WHERE id = ?',
                    (nickname, bio, _power, _zone, picture_url, _date.day, _date.month, _date.year, data['id_person_id'],)
                )
                db.commit()

        return render_template('auth/update.html', person = person)

    @bp.route('/<int:id>/delete', methods=('POST',))
    @login_required
    def delete(id):
        db = DbManager.get_db()
        db.execute('DELETE FROM user WHERE id = ?', (id,))
        db.commit()
        return redirect(url_for('blog.home'))
