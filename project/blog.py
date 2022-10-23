from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask.views import View

from werkzeug.exceptions import abort

from project.auth import login_required
from project.db import get_db


bp = Blueprint('blog', __name__)


class IndexView(View):
    init_every_request = False

    def __init__(self):
        self.template = 'blog/index.html'

    def dispatch_request(self):
        db = get_db()
        users = db.execute(
            'SELECT id, username'
            ' FROM user '
            ' ORDER BY id'
        ).fetchall()
        return render_template(self.template, users = users)

bp.add_url_rule(
    '/',
    view_func=IndexView.as_view('index')
)
