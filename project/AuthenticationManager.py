import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from project.DbManager import DbManager

from datetime import datetime

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
            _date = request.form['_date']

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
                        "INSERT INTO person (nickname, _role, bio, _power, _zone, picture_url) VALUES (?, ?, ?, ?, ?, ?)",
                        (nickname, 1, bio, _power, _zone, picture_url),
                    )
                    person = db.execute(
                                'SELECT * FROM person WHERE nickname = ?', (nickname,)
                            ).fetchone()
                    db.execute(
                        "INSERT INTO user (username, password, id_person_id, tier) VALUES (?, ?, ?, ?)",
                        (username, generate_password_hash(password), person['id'], tier),
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
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            nickname = request.form['nickname']
            tier = request.form['tier']
            bio = request.form['bio']
            _power = request.form['_power']
            _zone = request.form['_zone']
            picture_url = request.form['picture_url']
            _date = request.form['_date']
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

                data = db.execute('SELECT * FROM user WHERE id_person_id = ?', (id,)).fetchone()

                db.execute(
                    'UPDATE person SET nickname = ?, bio = ?, _power = ?, _zone = ?, picture_url = ?'
                    ' WHERE id = ?',
                    (nickname, bio, _power, _zone, picture_url, data['id_person_id'])
                )

                db.commit()
                return redirect(url_for('blog.index'))

        return render_template('auth/update.html')

    @bp.route('/<int:id>/delete', methods=('POST',))
    @login_required
    def delete(id):
        db = DbManager.get_db()
        db.execute('DELETE FROM user WHERE id = ?', (id,))
        db.commit()
        return redirect(url_for('blog.home'))
