import sqlite3

import click
from flask import current_app, g

class DbManager:

    @staticmethod
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db

    @staticmethod
    def close_db(e=None):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    @staticmethod
    def init_db():
        db = DbManager.get_db()

        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))


    @click.command('init-db')
    def init_db_command():
        """Clear the existing data and create new tables."""
        DbManager.init_db()
        click.echo('Initialized the database.')

    @staticmethod
    def init_app(app):
        app.teardown_appcontext(DbManager.close_db)
        app.cli.add_command(DbManager.init_db_command)

