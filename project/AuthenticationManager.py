import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from project.DbManager import DbManager

bp = Blueprint('auth', __name__, url_prefix='/auth')

class AuthenticationManager:
    @bp.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = DbManager.get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
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
        return redirect(url_for('index'))

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))

            return view(**kwargs)

        return wrapped_view

    @bp.route('/<int:id>/update', methods=('GET', 'POST'))
    @login_required
    def update(id):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'

            if error is not None:
                flash(error)
            else:
                db = DbManager.get_db()
                db.execute(
                    'UPDATE user SET username = ?, password= ?'
                    ' WHERE id = ?',
                    (username, generate_password_hash(password), id)
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
        return redirect(url_for('blog.index'))
