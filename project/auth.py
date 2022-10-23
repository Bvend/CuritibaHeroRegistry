import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.views import View

from werkzeug.security import check_password_hash, generate_password_hash

from project.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self):
        self.template = 'auth/register.html'
        self.db = get_db()

    def dispatch_request(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                try:
                    self.db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    self.db.commit()
                except self.db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    session.clear()
                    user = self.db.execute(
                                'SELECT * FROM user WHERE username = ?', (username,)
                            ).fetchone()
                    session['user_id'] = user['id']
                    return redirect(url_for('index'))

            flash(error)

        return render_template(self.template)

bp.add_url_rule(
    '/register',
    view_func=RegisterView.as_view('register')
)   


class LoginView(View):
    methods = ['GET', 'POST']

    def __init__(self):
        self.template = 'auth/login.html'
        self.db = get_db()

    def dispatch_request(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None
            user = self.db.execute(
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

        return render_template(self.template)

bp.add_url_rule(
    '/login',
    view_func=LoginView.as_view('login')
)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


class LogoutView(View):
    init_every_request = False

    def __init__(self):
        self.redirect_route = bp.name + '.login'

    def dispatch_request(self):
        session.clear()
        return redirect(url_for(self.redirect_route))

bp.add_url_rule(
    '/logout',
    view_func=LogoutView.as_view('logout')
)


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
            db = get_db()
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
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))