from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.DbManager import DbManager

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = DbManager.get_db()
    users = db.execute(
        'SELECT id, username'
        ' FROM user '
        ' ORDER BY id'
    ).fetchall()
    return render_template('blog/index.html', users = users)