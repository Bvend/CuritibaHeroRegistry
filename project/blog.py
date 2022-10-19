from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.auth import login_required
from project.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    users = db.execute(
        'SELECT id, username'
        ' FROM user '
        ' ORDER BY id'
    ).fetchall()
    return render_template('blog/index.html', users = users)